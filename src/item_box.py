from itertools import accumulate
import logging
from dataclasses import field

from ocp_vscode import show

from build123d import *
from partomatic import AutomatablePart, PartomaticConfig

from utils import stack_thickness
from parts import Partomatic, Card, CardBoxConfig


log = logging.getLogger(__name__)


class Standard(Card):
    width: int = 68
    height: int = 93

class SectionedConfig(PartomaticConfig):
    divider: float = 1.2
    card_stacks: list[int]

    @property
    def sections(self) -> list[float]:
        return [stack_thickness(c) for c in self.card_stacks]

    @property
    def section_walls(self) -> float:
        return (len(self.card_stacks) - 1) * self.divider

    @property
    def inside_floor(self) -> float:
        return sum(self.sections) + self.section_walls

class SectionedBoxConfig(SectionedConfig, CardBoxConfig):
    card: Standard = field(default_factory=Standard)

    # these defaults are for the `bosses` box
    name: str = "Bosses"
    color: str = "darkred"
    card_stacks: list[int] = field(default_factory=lambda: [26, 35, 78, 8, 11])

    @property
    def height(self) -> float:
        return super().height + self.wall

    @classmethod
    def footprint_height(cls):
        return super().footprint_height() + cls.wall

    @property
    def notch_floor(self) -> float:
        return self.height * 0.6


class Sectioned:
    def __init__(self, *args, **kwargs):
        stack = kwargs.pop("card_stacks", None)

        super().__init__(*args, **kwargs)

        if stack is not None:
            self.config.card_stacks = stack

    def _build_dividers(self):
        plane = self._divider_plane()

        with BuildSketch(plane) as s:
            with Locations( *self._divider_positions() ):
                self._make_divider_wall()

        extrude(s.sketch, amount=self.divider_height)

        along_wall = Axis(plane.origin, plane.y_dir)
        tops = edges(Select.LAST).filter_by(along_wall).group_by(Axis.Z)[-1]
        fillet(tops, radius=0.5)

    def _divider_plane(self):
        base = faces().filter_by(Plane.XY).sort_by(Axis.Z)[1]
        return Plane(base).shift_origin( base.position_at(0, 0.5) )

    def _divider_positions(self):
        return map(lambda pos: (pos, 0), accumulate(
            self.config.sections[1:-1],
            lambda x, y: x + y + self.config.divider,
            initial=self.config.sections[0]) )

    def _make_divider_wall(self):
        _align = (Align.MIN, Align.CENTER)
        Rectangle(self.config.divider, self.config.card.width, align=_align)

    def is_sectioned(self):
        return len(self.config.sections) > 1


class SectionedBox(Sectioned, Partomatic):
    config: SectionedBoxConfig = SectionedBoxConfig()

    def compile(self):
        self.parts.clear()

        with BuildPart() as box:
            self._build_shell()

            self._carve_notch()
            self._fillet_shell()

            if self.is_sectioned():
                self._build_dividers()


        box.part.color = Color(self.config.color)
        self.parts.append(AutomatablePart(
            box.part, f"{self.config.name} card-box.stl",
            display_location=Location((0, 0, 0)),
            stl_folder=self.config.stl_folder,
        ))

    def _build_shell(self):
        with BuildSketch(Plane.XY) as base:
            Rectangle(self.config.inside_floor, self.config.card.width)
        extrude(base.sketch, amount=self.config.wall)

        offset_kwargs = dict(kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)
        with BuildSketch(Plane.XY) as walls:
            outline = Rectangle(self.config.depth, self.config.face)
            offset(outline, -self.config.wall, **offset_kwargs)
        extrude(walls.sketch, amount=self.config.height)

    def _carve_notch(self):
        face = faces().filter_by(Plane.YZ).sort_by(Axis.X)[-1]
        pos = face.position_at(1, 0)

        with BuildSketch( Plane(face).shift_origin(pos) ) as s:
            x = self.config.face
            y = self.config.height - self.config.notch_floor

            Polygon(
                (0, 0),
                (0, -y),
                (-x * 0.10, -y),
                (-x * 0.55, 0),
            )
        extrude(s.sketch, amount=-self.config.depth, mode=Mode.SUBTRACT)

    def _fillet_shell(self):
        _vert = edges().filter_by(Axis.Z).group_by(Axis.X)
        _inner_corners = edges().filter_by(Plane.XY).group_by(Axis.Z)[1]
        fillet( edges() - _inner_corners - _vert[1] - _vert[-2], radius=1 )

    @property
    def divider_height(self):
        # extra -.5 is to align juuuuuust underneath the box rim
        return self.config.notch_floor - self.config.wall - .5


if __name__ == "__main__":
    box = SectionedBox()
    box.compile()
    show(box.assembly(), show_sketch_local=False)

    log.info("SectionedBox should be loaded")
