import dataclasses
import copy
import abc
import typing
import collections.abc

import momapy.drawing
import momapy.styling
import momapy.positioning
import momapy.geometry
import momapy.builder

renderers = {}


def register_renderer(name, renderer_cls):
    """Register a renderer class"""
    renderers[name] = renderer_cls


def render_map(
    map_: momapy.core.Map,
    output_file: str,
    format_: str = "pdf",
    renderer: str = "skia",
    style_sheet: momapy.styling.StyleSheet | None = None,
    to_top_left: bool = False,
):
    """Render a map to a file in a given format and with a given registered renderer"""
    maps = [map_]
    render_maps(maps, output_file, format_, renderer, style_sheet, to_top_left)


def render_maps(
    maps: collections.abc.Collection[momapy.core.Map],
    output_file: str,
    format_: str = "pdf",
    renderer: str = "skia",
    style_sheet: momapy.styling.StyleSheet | None = None,
    to_top_left: bool = False,
    multi_pages: bool = True,
):
    """Render a collection of maps to a file in a given format and with a given registered renderer"""

    def _prepare_maps(maps, style_sheet=None, to_top_left=False):
        bboxes = [map_.layout.self_bbox() for map_ in maps]
        bbox = momapy.positioning.fit(bboxes)
        max_x = bbox.x + bbox.width / 2
        max_y = bbox.y + bbox.height / 2
        if style_sheet is not None or to_top_left:
            new_maps = []
            for map_ in maps:
                if isinstance(map_, momapy.core.Map):
                    new_maps.append(momapy.builder.builder_from_object(map_))
                elif isinstance(map_, momapy.core.MapBuilder):
                    new_maps.append(copy.deepcopy(map_))
            maps = new_maps
        if style_sheet is not None:
            if (
                not isinstance(style_sheet, collections.abc.Collection)
                or isinstance(style_sheet, str)
                or isinstance(style_sheet, momapy.styling.StyleSheet)
            ):
                style_sheets = [style_sheet]
            else:
                style_sheets = style_sheet
            style_sheets = [
                (
                    momapy.styling.StyleSheet.from_file(style_sheet)
                    if not isinstance(style_sheet, momapy.styling.StyleSheet)
                    else style_sheet
                )
                for style_sheet in style_sheets
            ]
            style_sheet = momapy.styling.combine_style_sheets(style_sheets)
            for map_ in maps:
                momapy.styling.apply_style_sheet(map_.layout, style_sheet)
        if to_top_left:
            min_x = bbox.x - bbox.width / 2
            min_y = bbox.y - bbox.height / 2
            max_x -= min_x
            max_y -= min_y
            translation = momapy.geometry.Translation(-min_x, -min_y)
            for map_ in maps:
                if map_.layout.transform is None:
                    map_.layout.transform = momapy.core.TupleBuilder()
                map_.layout.transform.append(translation)
        return maps, max_x, max_y

    if not multi_pages:
        maps, max_x, max_y = _prepare_maps(maps, style_sheet, to_top_left)
        renderer = renderers[renderer].from_file(
            output_file, max_x, max_y, format_
        )
        renderer.begin_session()
        for map_ in maps:
            renderer.render_map(map_)
        renderer.end_session()
    else:
        for i, map_ in enumerate(maps):
            maps, max_x, max_y = _prepare_maps(
                [map_], style_sheet, to_top_left
            )
            map_ = maps[0]
            if i == 0:
                renderer = renderers[renderer].from_file(
                    output_file, max_x, max_y, format_
                )
                renderer.begin_session()
            else:
                renderer.new_page(max_x, max_y)
            renderer.render_map(map_)
        renderer.end_session()


@dataclasses.dataclass
class Renderer(abc.ABC):
    """Abstract class for renderers"""

    initial_values: typing.ClassVar[dict] = {
        "font_family": "Arial",
        "font_weight": 16.0,
    }
    font_weight_value_mapping: typing.ClassVar[dict] = {
        momapy.drawing.FontWeight.NORMAL: 400,
        momapy.drawing.FontWeight.BOLD: 700,
    }

    @abc.abstractmethod
    def begin_session(self):
        """Begin a session"""
        pass

    @abc.abstractmethod
    def end_session(self):
        """End a session"""
        pass

    @abc.abstractmethod
    def new_page(self, width, height):
        """Make a new page"""
        pass

    @abc.abstractmethod
    def render_map(self, map_: momapy.core.Map):
        """Render a map"""
        pass

    @abc.abstractmethod
    def render_layout_element(self, layout_element: momapy.core.LayoutElement):
        """Render a layout element"""
        pass

    @abc.abstractmethod
    def render_drawing_element(
        self, drawing_element: momapy.drawing.DrawingElement
    ):
        """Render a drawing element"""
        pass

    @classmethod
    def get_lighter_font_weight(
        cls, font_weight: momapy.drawing.FontWeight | float
    ) -> float:
        """Return the boldest font weight lighter than the given font weight"""
        if isinstance(font_weight, momapy.drawing.FontWeight):
            font_weight = cls.font_weight_value_mapping.get(font_weight)
            if font_weight is None:
                raise ValueError(
                    f"font weight must be a float, {momapy.drawing.FontWeight.NORMAL}, or {momapy.drawing.FontWeight.BOLD}"
                )
        if font_weight > 700:
            new_font_weight = 700
        elif font_weight > 500:
            new_font_weight = 400
        else:
            new_font_weight = 100
        return new_font_weight

    @classmethod
    def get_bolder_font_weight(
        cls, font_weight: momapy.drawing.FontWeight | float
    ) -> float:
        """Return the lightest font weight bolder than the given font weight"""
        if isinstance(font_weight, momapy.drawing.FontWeight):
            font_weight = cls.font_weight_value_mapping.get(font_weight)
            if font_weight is None:
                raise ValueError(
                    f"font weight must be a float, {momapy.drawing.FontWeight.NORMAL}, or {momapy.drawing.FontWeight.BOLD}"
                )
        if font_weight < 400:
            new_font_weight = 400
        elif font_weight < 600:
            new_font_weight = 700
        else:
            new_font_weight = 900
        return new_font_weight


@dataclasses.dataclass
class StatefulRenderer(Renderer):
    """Abstract class for stateful renderers"""

    _current_state: dict = dataclasses.field(default_factory=dict)
    _states: list[dict] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self._initialize_current_state()

    @abc.abstractmethod
    def self_save(self):
        pass

    @abc.abstractmethod
    def self_restore(self):
        pass

    @classmethod
    def _make_initial_current_state(cls):
        state = {}
        for (
            attr_name,
            attr_d,
        ) in momapy.drawing.PRESENTATION_ATTRIBUTES.items():
            if attr_name in cls.initial_values:
                attr_value = cls.initial_values[attr_name]
            else:
                attr_value = attr_d["initial"]
            state[attr_name] = attr_value
        return state

    def _initialize_current_state(self):
        state = self._make_initial_current_state()
        self.set_current_state(state)

    def save(self):
        """Save the current state"""
        self._states.append(copy.deepcopy(self.get_current_state()))
        self.self_save()

    def restore(self):
        """Set the current state to the last saved"""
        if len(self._states) > 0:
            state = self._states.pop()
            self.set_current_state(state)
            self.self_restore()
        else:
            raise Exception("no state to be restored")

    def get_initial_value(self, attr_name: str) -> typing.Any:
        """Return the initial value for an attribute"""
        attr_value = self.initial_values.get(attr_name)
        if attr_value is None:
            attr_d = momapy.drawing.PRESENTATION_ATTRIBUTES[attr_name]
            attr_value = attr_d["initial"]
            if attr_value is None:
                attr_value = momapy.drawing.INITIAL_VALUES[attr_name]
        return attr_value

    def get_current_value(self, attr_name: str) -> typing.Any:
        """Return the current value for an attribute"""
        return self.get_current_state()[attr_name]

    def get_current_state(self) -> dict[str, typing.Any]:
        """Return the current state"""
        return self._current_state

    def set_current_value(self, attr_name: str, attr_value: typing.Any):
        """Set the current value for an attribute"""
        if attr_value is None:
            attr_d = momapy.drawing.PRESENTATION_ATTRIBUTES[attr_name]
            if not attr_d["inherited"]:
                attr_value = self.initial_values.get(attr_name)
                if attr_value is None:
                    attr_value = attr_d["initial"]
                if attr_value is None:
                    attr_value = momapy.drawing.INITIAL_VALUES[attr_name]
        if attr_name == "font_weight":
            if isinstance(attr_value, momapy.drawing.FontWeight):
                if (
                    attr_value == momapy.drawing.FontWeight.NORMAL
                    or attr_value == momapy.drawing.FontWeight.BOLD
                ):
                    attr_value = self.font_weight_value_mapping[attr_value]
                elif attr_value == momapy.drawing.FontWeight.BOLDER:
                    attr_value = self.get_bolder_font_weight(
                        self.get_current_value("font_weight")
                    )
                elif attr_value == momapy.drawing.FontWeight.LIGHTER:
                    attr_value = self.get_lighter_font_weight(
                        self.get_current_value("font_weight")
                    )
        if attr_value is not None:
            self._current_state[attr_name] = attr_value

    def set_current_state(self, state: dict):
        """Set the current state to a given state"""
        for attr_name, attr_value in state.items():
            self.set_current_value(attr_name, attr_value)

    def _get_state_from_drawing_element(self, drawing_element):
        state = {}
        for attr_name in momapy.drawing.PRESENTATION_ATTRIBUTES:
            state[attr_name] = getattr(drawing_element, attr_name)
        return state

    def set_current_state_from_drawing_element(
        self, drawing_element: momapy.drawing.DrawingElement
    ):
        """Set the current state to a state given by a drawing element"""
        state = self._get_state_from_drawing_element(drawing_element)
        self.set_current_state(state)
