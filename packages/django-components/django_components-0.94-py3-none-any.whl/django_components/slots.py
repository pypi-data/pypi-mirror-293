import difflib
import json
import re
from collections import deque
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django.template import Context, Template
from django.template.base import FilterExpression, Node, NodeList, Parser, TextNode
from django.template.defaulttags import CommentNode
from django.template.exceptions import TemplateSyntaxError
from django.utils.safestring import SafeString, mark_safe

from django_components.app_settings import ContextBehavior
from django_components.context import (
    _FILLED_SLOTS_CONTENT_CONTEXT_KEY,
    _INJECT_CONTEXT_KEY_PREFIX,
    _REGISTRY_CONTEXT_KEY,
    _ROOT_CTX_CONTEXT_KEY,
)
from django_components.expression import RuntimeKwargs, is_identifier
from django_components.logger import trace_msg
from django_components.node import BaseNode, NodeTraverse, nodelist_has_content, walk_nodelist

if TYPE_CHECKING:
    from django_components.component_registry import ComponentRegistry

TSlotData = TypeVar("TSlotData", bound=Mapping, contravariant=True)

DEFAULT_SLOT_KEY = "_DJANGO_COMPONENTS_DEFAULT_SLOT"
SLOT_DATA_KWARG = "data"
SLOT_NAME_KWARG = "name"
SLOT_DEFAULT_KWARG = "default"
SLOT_REQUIRED_KEYWORD = "required"
SLOT_DEFAULT_KEYWORD = "default"


# Public types
SlotResult = Union[str, SafeString]


class SlotFunc(Protocol, Generic[TSlotData]):
    def __call__(self, ctx: Context, slot_data: TSlotData, slot_ref: "SlotRef") -> SlotResult: ...  # noqa E704


SlotContent = Union[SlotResult, SlotFunc[TSlotData]]

# Internal type aliases
SlotId = str
SlotName = str
SlotDefaultName = str
SlotDataName = str


@dataclass(frozen=True)
class FillContent(Generic[TSlotData]):
    """
    This represents content set with the `{% fill %}` tag, e.g.:

    ```django
    {% component "my_comp" %}
        {% fill "first_slot" %} <--- This
            hi
            {{ my_var }}
            hello
        {% endfill %}
    {% endcomponent %}
    ```
    """

    content_func: SlotFunc[TSlotData]
    slot_default_var: Optional[SlotDefaultName]
    slot_data_var: Optional[SlotDataName]


class Slot(NamedTuple):
    """
    This represents content set with the `{% slot %}` tag, e.g.:

    ```django
    {% slot "my_comp" default %} <--- This
        hi
        {{ my_var }}
        hello
    {% endslot %}
    ```
    """

    id: str
    name: str
    is_default: bool
    is_required: bool
    nodelist: NodeList


@dataclass(frozen=True)
class SlotFill(Generic[TSlotData]):
    """
    SlotFill describes what WILL be rendered.

    It is a Slot that has been resolved against FillContents passed to a Component.
    """

    name: str
    escaped_name: str
    is_filled: bool
    content_func: SlotFunc[TSlotData]
    context_data: Mapping
    slot_default_var: Optional[SlotDefaultName]
    slot_data_var: Optional[SlotDataName]


class SlotRef:
    """
    SlotRef allows to treat a slot as a variable. The slot is rendered only once
    the instance is coerced to string.

    This is used to access slots as variables inside the templates. When a SlotRef
    is rendered in the template with `{{ my_lazy_slot }}`, it will output the contents
    of the slot.
    """

    def __init__(self, slot: "SlotNode", context: Context):
        self._slot = slot
        self._context = context

    # Render the slot when the template coerces SlotRef to string
    def __str__(self) -> str:
        return mark_safe(self._slot.nodelist.render(self._context))


class SlotNode(BaseNode):
    def __init__(
        self,
        nodelist: NodeList,
        trace_id: str,
        node_id: Optional[str] = None,
        kwargs: Optional[RuntimeKwargs] = None,
        is_required: bool = False,
        is_default: bool = False,
    ):
        super().__init__(nodelist=nodelist, args=None, kwargs=kwargs, node_id=node_id)

        self.is_required = is_required
        self.is_default = is_default
        self.trace_id = trace_id

    @property
    def active_flags(self) -> List[str]:
        flags = []
        if self.is_required:
            flags.append("required")
        if self.is_default:
            flags.append("default")
        return flags

    def __repr__(self) -> str:
        return f"<Slot Node: {self.node_id}. Contents: {repr(self.nodelist)}. Options: {self.active_flags}>"

    def render(self, context: Context) -> SafeString:
        trace_msg("RENDR", "SLOT", self.trace_id, self.node_id)
        slots: Dict[SlotId, "SlotFill"] = context[_FILLED_SLOTS_CONTENT_CONTEXT_KEY]
        # NOTE: Slot entry MUST be present. If it's missing, there was an issue upstream.
        slot_fill = slots[self.node_id]

        name, kwargs = self.resolve_kwargs(context)

        extra_context: Dict[str, Any] = {}

        # Irrespective of which context we use ("root" context or the one passed to this
        # render function), pass down the keys used by inject/provide feature. This makes it
        # possible to pass the provided values down the slots, e.g.:
        # {% provide "abc" val=123 %}
        #   {% slot "content" %}{% endslot %}
        # {% endprovide %}
        for key, value in context.flatten().items():
            if key.startswith(_INJECT_CONTEXT_KEY_PREFIX):
                extra_context[key] = value

        # If slot fill is using `{% fill "myslot" default="abc" %}`, then set the "abc" to
        # the context, so users can refer to the default slot from within the fill content.
        slot_ref = SlotRef(self, context)
        default_var = slot_fill.slot_default_var
        if default_var:
            if not default_var.isidentifier():
                raise TemplateSyntaxError(
                    f"Slot default alias in fill '{name}' must be a valid identifier. Got '{default_var}'"
                )
            extra_context[default_var] = slot_ref

        # Expose the kwargs that were passed to the `{% slot %}` tag. These kwargs
        # are made available through a variable name that was set on the `{% fill %}`
        # tag.
        data_var = slot_fill.slot_data_var
        if data_var:
            if not data_var.isidentifier():
                raise TemplateSyntaxError(
                    f"Slot data alias in fill '{name}' must be a valid identifier. Got '{data_var}'"
                )
            extra_context[data_var] = kwargs

        # For the user-provided slot fill, we want to use the context of where the slot
        # came from (or current context if configured so)
        used_ctx = self._resolve_slot_context(context, slot_fill)
        with used_ctx.update(extra_context):
            # Render slot as a function
            # NOTE: While `{% fill %}` tag has to opt in for the `default` and `data` variables,
            #       the render function ALWAYS receives them.
            output = slot_fill.content_func(used_ctx, kwargs, slot_ref)

        trace_msg("RENDR", "SLOT", self.trace_id, self.node_id, msg="...Done!")
        return output

    def _resolve_slot_context(self, context: Context, slot_fill: "SlotFill") -> Context:
        """Prepare the context used in a slot fill based on the settings."""
        # If slot is NOT filled, we use the slot's default AKA content between
        # the `{% slot %}` tags. These should be evaluated as if the `{% slot %}`
        # tags weren't even there, which means that we use the current context.
        if not slot_fill.is_filled:
            return context

        registry: "ComponentRegistry" = context[_REGISTRY_CONTEXT_KEY]
        if registry.settings.CONTEXT_BEHAVIOR == ContextBehavior.DJANGO:
            return context
        elif registry.settings.CONTEXT_BEHAVIOR == ContextBehavior.ISOLATED:
            return context[_ROOT_CTX_CONTEXT_KEY]
        else:
            raise ValueError(f"Unknown value for CONTEXT_BEHAVIOR: '{registry.settings.CONTEXT_BEHAVIOR}'")

    def resolve_kwargs(
        self,
        context: Context,
        component_name: Optional[str] = None,
    ) -> Tuple[str, Dict[str, Optional[str]]]:
        kwargs = self.kwargs.resolve(context)
        name = kwargs.pop(SLOT_NAME_KWARG, None)

        if not name:
            raise RuntimeError(f"Slot tag kwarg 'name' is missing in component {component_name}")

        return (name, kwargs)


class FillNode(BaseNode):
    """
    Set when a `component` tag pair is passed template content that
    excludes `fill` tags. Nodes of this type contribute their nodelists to slots marked
    as 'default'.
    """

    def __init__(
        self,
        nodelist: NodeList,
        kwargs: RuntimeKwargs,
        trace_id: str,
        node_id: Optional[str] = None,
        is_implicit: bool = False,
    ):
        super().__init__(nodelist=nodelist, args=None, kwargs=kwargs, node_id=node_id)

        self.is_implicit = is_implicit
        self.trace_id = trace_id
        self.component_id: Optional[str] = None

    def render(self, context: Context) -> str:
        raise TemplateSyntaxError(
            "{% fill ... %} block cannot be rendered directly. "
            "You are probably seeing this because you have used one outside "
            "a {% component %} context."
        )

    def __repr__(self) -> str:
        return f"<{type(self)} ID: {self.node_id}. Contents: {repr(self.nodelist)}.>"

    def resolve_kwargs(self, context: Context, component_name: Optional[str] = None) -> Dict[str, Optional[str]]:
        kwargs = self.kwargs.resolve(context)

        name = self._resolve_kwarg(kwargs, SLOT_NAME_KWARG, "slot name", component_name, identifier=False)
        default_key = self._resolve_kwarg(kwargs, SLOT_DEFAULT_KWARG, "slot default", component_name)
        data_key = self._resolve_kwarg(kwargs, SLOT_DATA_KWARG, "slot data", component_name)

        # data and default cannot be bound to the same variable
        if data_key and default_key and data_key == default_key:
            raise RuntimeError(
                f"Fill '{name}' received the same string for slot default ({SLOT_DEFAULT_KWARG}=...)"
                f" and slot data ({SLOT_DATA_KWARG}=...)"
            )

        return {
            SLOT_NAME_KWARG: name,
            SLOT_DEFAULT_KWARG: default_key,
            SLOT_DATA_KWARG: data_key,
        }

    def _resolve_kwarg(
        self,
        kwargs: Dict[str, Any],
        key: str,
        name: str,
        component_name: Optional[str] = None,
        identifier: bool = True,
    ) -> Optional[str]:
        if key not in kwargs:
            return None

        value = kwargs[key]
        if identifier and not is_identifier(value):
            raise RuntimeError(
                f"Fill tag {name} in component {component_name}"
                f"does not resolve to a valid Python identifier, got '{value}'"
            )
        elif not identifier and not value:
            raise RuntimeError(f"Fill tag {name} is missing value in component {component_name}")

        return value


def parse_slot_fill_nodes_from_component_nodelist(
    component_nodelist: NodeList,
    ComponentNodeCls: Type[Node],
) -> List[FillNode]:
    """
    Given a component body (`django.template.NodeList`), find all slot fills,
    whether defined explicitly with `{% fill %}` or implicitly.

    So if we have a component body:
    ```django
    {% component "mycomponent" %}
        {% fill "first_fill" %}
            Hello!
        {% endfill %}
        {% fill "second_fill" %}
            Hello too!
        {% endfill %}
    {% endcomponent %}
    ```
    Then this function returns the nodes (`django.template.Node`) for `fill "first_fill"`
    and `fill "second_fill"`.
    """
    fill_nodes: List[FillNode] = []
    if nodelist_has_content(component_nodelist):
        for parse_fn in (
            _try_parse_as_default_fill,
            _try_parse_as_named_fill_tag_set,
        ):
            curr_fill_nodes = parse_fn(component_nodelist, ComponentNodeCls)
            if curr_fill_nodes:
                fill_nodes = curr_fill_nodes
                break
        else:
            raise TemplateSyntaxError(
                "Illegal content passed to 'component' tag pair. "
                "Possible causes: 1) Explicit 'fill' tags cannot occur alongside other "
                "tags except comment tags; 2) Default (default slot-targeting) content "
                "is mixed with explict 'fill' tags."
            )
    return fill_nodes


def _try_parse_as_named_fill_tag_set(
    nodelist: NodeList,
    ComponentNodeCls: Type[Node],
) -> List[FillNode]:
    result = []
    seen_names: Set[str] = set()
    for node in nodelist:
        if isinstance(node, FillNode):
            # If the fill name was defined statically, then check for no duplicates.
            maybe_fill_name = node.kwargs.kwargs.get(SLOT_NAME_KWARG)
            if isinstance(maybe_fill_name, FilterExpression):
                if maybe_fill_name.token in seen_names:
                    raise TemplateSyntaxError(
                        f"Multiple fill tags cannot target the same slot name: "
                        f"Detected duplicate fill tag name '{maybe_fill_name.token}'."
                    )
                seen_names.add(maybe_fill_name.token)
            result.append(node)
        elif isinstance(node, CommentNode):
            pass
        elif isinstance(node, TextNode) and node.s.isspace():
            pass
        else:
            return []
    return result


def _try_parse_as_default_fill(
    nodelist: NodeList,
    ComponentNodeCls: Type[Node],
) -> List[FillNode]:
    nodes_stack: List[Node] = list(nodelist)
    while nodes_stack:
        node = nodes_stack.pop()
        if isinstance(node, FillNode):
            return []
        elif isinstance(node, ComponentNodeCls):
            # Stop searching here, as fill tags are permitted inside component blocks
            # embedded within a default fill node.
            continue
        for nodelist_attr_name in node.child_nodelists:
            nodes_stack.extend(getattr(node, nodelist_attr_name, []))
    else:
        return [
            FillNode(
                nodelist=nodelist,
                kwargs=RuntimeKwargs(
                    {
                        # Wrap the default slot name in quotes so it's treated as FilterExpression
                        SLOT_NAME_KWARG: FilterExpression(json.dumps(DEFAULT_SLOT_KEY), Parser("")),
                    }
                ),
                is_implicit=True,
                trace_id="default",
            )
        ]


def resolve_fill_nodes(
    context: Context,
    fill_nodes: List[FillNode],
    component_name: str,
) -> Dict[str, FillContent]:
    fill_content: Dict[str, FillContent] = {}
    for fill_node in fill_nodes:
        # Note that outer component context is used to resolve variables in
        # fill tag.
        fill_kwargs = fill_node.resolve_kwargs(context, component_name)
        fill_name = fill_kwargs.get(SLOT_NAME_KWARG)

        if SLOT_NAME_KWARG not in fill_kwargs:
            raise TemplateSyntaxError("Fill tag is missing the 'name' kwarg")

        if not isinstance(fill_name, str):
            raise TemplateSyntaxError(f"Fill tag 'name' kwarg must resolve to a string, got {fill_name}")

        if fill_name in fill_content:
            raise TemplateSyntaxError(
                f"Multiple fill tags cannot target the same slot name: "
                f"Detected duplicate fill tag name '{fill_name}'."
            )

        fill_content[fill_name] = FillContent(
            content_func=_nodelist_to_slot_render_func(fill_node.nodelist),
            slot_default_var=fill_kwargs[SLOT_DEFAULT_KWARG],
            slot_data_var=fill_kwargs[SLOT_DATA_KWARG],
        )
    return fill_content


####################
# SLOT RESOLUTION
####################


def resolve_slots(
    context: Context,
    template: Template,
    component_name: Optional[str],
    context_data: Mapping[str, Any],
    fill_content: Dict[SlotName, FillContent],
) -> Tuple[Dict[SlotId, Slot], Dict[SlotId, SlotFill]]:
    """
    Search the template for all SlotNodes, and associate the slots
    with the given fills.

    Returns tuple of:
    - Slots defined in the component's Template with `{% slot %}` tag
    - SlotFills (AKA slots matched with fills) describing what will be rendered for each slot.
    """
    slot_fills = {
        name: SlotFill(
            name=name,
            escaped_name=_escape_slot_name(name),
            is_filled=True,
            content_func=fill.content_func,
            context_data=context_data,
            slot_default_var=fill.slot_default_var,
            slot_data_var=fill.slot_data_var,
        )
        for name, fill in fill_content.items()
    }

    slots: Dict[SlotId, Slot] = {}
    # This holds info on which slot (key) has which slots nested in it (value list)
    slot_children: Dict[SlotId, List[SlotId]] = {}

    def on_node(entry: NodeTraverse) -> None:
        node = entry.node
        if not isinstance(node, SlotNode):
            return

        slot_name, _ = node.resolve_kwargs(context, component_name)

        # 1. Collect slots
        # Basically we take all the important info form the SlotNode, so the logic is
        # less coupled to Django's Template/Node. Plain tuples should also help with
        # troubleshooting.
        slot = Slot(
            id=node.node_id,
            name=slot_name,
            nodelist=node.nodelist,
            is_default=node.is_default,
            is_required=node.is_required,
        )
        slots[node.node_id] = slot

        # 2. Figure out which Slots are nested in other Slots, so we can render
        # them from outside-inwards, so we can skip inner Slots if fills are provided.
        # We should end up with a graph-like data like:
        # - 0001: [0002]
        # - 0002: []
        # - 0003: [0004]
        # In other words, the data tells us that slot ID 0001 is PARENT of slot 0002.
        curr_entry = entry.parent
        while curr_entry and curr_entry.parent is not None:
            if not isinstance(curr_entry.node, SlotNode):
                curr_entry = curr_entry.parent
                continue

            parent_slot_id = curr_entry.node.node_id
            if parent_slot_id not in slot_children:
                slot_children[parent_slot_id] = []
            slot_children[parent_slot_id].append(node.node_id)
            break

    walk_nodelist(template.nodelist, on_node, context)

    # 3. Figure out which slot the default/implicit fill belongs to
    slot_fills = _resolve_default_slot(
        template_name=template.name,
        component_name=component_name,
        slots=slots,
        slot_fills=slot_fills,
    )

    # 4. Detect any errors with slots/fills
    _report_slot_errors(slots, slot_fills, component_name)

    # 5. Find roots of the slot relationships
    top_level_slot_ids: List[SlotId] = []
    for node_id, slot in slots.items():
        if node_id not in slot_children or not slot_children[node_id]:
            top_level_slot_ids.append(node_id)

    # 6. Walk from out-most slots inwards, and decide whether and how
    # we will render each slot.
    resolved_slots: Dict[SlotId, SlotFill] = {}
    slot_ids_queue = deque([*top_level_slot_ids])
    while len(slot_ids_queue):
        slot_id = slot_ids_queue.pop()
        slot = slots[slot_id]

        # Check if there is a slot fill for given slot name
        if slot.name in slot_fills:
            # If yes, we remember which slot we want to replace with already-rendered fills
            resolved_slots[slot_id] = slot_fills[slot.name]
            # Since the fill cannot include other slots, we can leave this path
            continue
        else:
            # If no, then the slot is NOT filled, and we will render the slot's default (what's
            # between the slot tags)
            resolved_slots[slot_id] = SlotFill(
                name=slot.name,
                escaped_name=_escape_slot_name(slot.name),
                is_filled=False,
                content_func=_nodelist_to_slot_render_func(slot.nodelist),
                context_data=context_data,
                slot_default_var=None,
                slot_data_var=None,
            )
            # Since the slot's default CAN include other slots (because it's defined in
            # the same template), we need to enqueue the slot's children
            if slot_id in slot_children and slot_children[slot_id]:
                slot_ids_queue.extend(slot_children[slot_id])

    # By the time we get here, we should know, for each slot, how it will be rendered
    # -> Whether it will be replaced with a fill, or whether we render slot's defaults.
    return slots, resolved_slots


def _resolve_default_slot(
    template_name: str,
    component_name: Optional[str],
    slots: Dict[SlotId, Slot],
    slot_fills: Dict[SlotName, SlotFill],
) -> Dict[SlotName, SlotFill]:
    """Figure out which slot the default fill refers to, and perform checks."""
    named_fills = slot_fills.copy()

    if DEFAULT_SLOT_KEY in named_fills:
        default_fill = named_fills.pop(DEFAULT_SLOT_KEY)
    else:
        default_fill = None

    default_slot_encountered: bool = False

    # Check for errors
    for slot in slots.values():
        if slot.is_default:
            if default_slot_encountered:
                raise TemplateSyntaxError(
                    "Only one component slot may be marked as 'default'. "
                    f"To fix, check template '{template_name}' "
                    f"of component '{component_name}'."
                )
            default_slot_encountered = True

            # Here we've identified which slot the default/implicit fill belongs to
            if default_fill:
                # NOTE: We recreate new instance, passing all fields, instead of using
                # `NamedTuple._replace`, because `_replace` is not typed.
                named_fills[slot.name] = SlotFill(
                    is_filled=default_fill.is_filled,
                    content_func=default_fill.content_func,
                    context_data=default_fill.context_data,
                    slot_default_var=default_fill.slot_default_var,
                    slot_data_var=default_fill.slot_data_var,
                    # Updated fields
                    name=slot.name,
                    escaped_name=_escape_slot_name(slot.name),
                )

    # Check: Only component templates that include a 'default' slot
    # can be invoked with implicit filling.
    if default_fill and not default_slot_encountered:
        raise TemplateSyntaxError(
            f"Component '{component_name}' passed default fill content '{default_fill.name}'"
            f"(i.e. without explicit 'fill' tag), "
            f"even though none of its slots is marked as 'default'."
        )

    return named_fills


def _report_slot_errors(
    slots: Dict[SlotId, Slot],
    slot_fills: Dict[SlotName, SlotFill],
    registered_name: Optional[str],
) -> None:
    slots_by_name = {slot.name: slot for slot in slots.values()}
    unfilled_slots: Set[str] = {slot.name for slot in slots.values() if slot.name not in slot_fills}
    unmatched_fills: Set[str] = {
        slot_fill.name for slot_fill in slot_fills.values() if slot_fill.name not in slots_by_name
    }
    required_slot_names: Set[str] = set([slot.name for slot in slots.values() if slot.is_required])

    # Check that 'required' slots are filled.
    for slot_name in unfilled_slots:
        if slot_name in required_slot_names:
            msg = (
                f"Slot '{slot_name}' is marked as 'required' (i.e. non-optional), "
                f"yet no fill is provided. Check template.'"
            )
            if unmatched_fills:
                msg = f"{msg}\nPossible typo in unresolvable fills: {unmatched_fills}."
            raise TemplateSyntaxError(msg)

    # Check that all fills can be matched to a slot on the component template.
    # To help with easy-to-overlook typos, we fuzzy match unresolvable fills to
    # those slots for which no matching fill was encountered. In the event of
    # a close match, we include the name of the matched unfilled slot as a
    # hint in the error message.
    #
    # Note: Finding a good `cutoff` value may require further trial-and-error.
    # Higher values make matching stricter. This is probably preferable, as it
    # reduces false positives.
    for fill_name in unmatched_fills:
        fuzzy_slot_name_matches = difflib.get_close_matches(fill_name, unfilled_slots, n=1, cutoff=0.7)
        msg = (
            f"Component '{registered_name}' passed fill that refers to undefined slot:"
            f" '{fill_name}'."
            f"\nUnfilled slot names are: {sorted(unfilled_slots)}."
        )
        if fuzzy_slot_name_matches:
            msg += f"\nDid you mean '{fuzzy_slot_name_matches[0]}'?"
        raise TemplateSyntaxError(msg)


name_escape_re = re.compile(r"[^\w]")


def _escape_slot_name(name: str) -> str:
    """
    Users may define slots with names which are invalid identifiers like 'my slot'.
    But these cannot be used as keys in the template context, e.g. `{{ component_vars.is_filled.'my slot' }}`.
    So as workaround, we instead use these escaped names which are valid identifiers.

    So e.g. `my slot` should be escaped as `my_slot`.
    """
    # NOTE: Do a simple substitution where we replace all non-identifier characters with `_`.
    # Identifiers consist of alphanum (a-zA-Z0-9) and underscores.
    # We don't check if these escaped names conflict with other existing slots in the template,
    # we leave this obligation to the user.
    escaped_name = name_escape_re.sub("_", name)
    return escaped_name


def _nodelist_to_slot_render_func(nodelist: NodeList) -> SlotFunc:
    def render_func(ctx: Context, kwargs: Dict[str, Any], slot_ref: SlotRef) -> SlotResult:
        return nodelist.render(ctx)

    return render_func  # type: ignore[return-value]
