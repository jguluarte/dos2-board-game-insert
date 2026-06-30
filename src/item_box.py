from itertools import accumulate
import logging
from dataclasses import field

from ocp_vscode import show

from build123d import *
from partomatic import AutomatablePart

from utils import stack_thickness
from parts import Partomatic, Card, CardBoxConfig


log = logging.getLogger(__name__)


class Standard(Card):
    width: int = 68
    height: int = 93

class SectionedBoxConfig(CardBoxConfig):
    divider: float = 1.2
    card: Standard = field(default_factory=Standard)

    # these defaults are for the `bosses` box
    name: str = "Bosses"
    card_stacks: list[int] = field(default_factory=lambda: [26, 35, 78, 8, 11])

    @property
    def sections(self) -> list[float]:
        return [stack_thickness(c) for c in self.card_stacks]

    @property
    def section_walls(self) -> float:
        return (len(self.card_stacks) - 1) * self.divider

    @property
    def inside_floor(self) -> float:
        return sum(self.sections) + self.section_walls


class SectionedBox(Partomatic):
    config: SectionedBoxConfig = SectionedBoxConfig()

    def compile(self):
        self.parts.clear()

        log.info(self.config.sections)

        with BuildPart() as box:
            # base
            with BuildSketch(Plane.XY):
                Rectangle(self.config.inside_floor, self.config.card.width)
            extrude(amount=self.config.wall)

            # walls
            with BuildSketch(Plane.XY):
                walls = Rectangle(self.config.depth, self.config.face)
                offset(walls, -self.config.wall, kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)
            extrude(amount=self.config.height)

            if self.is_sectioned():
                base = faces().filter_by(Plane.XY).sort_by(Axis.Z)[1]
                pos = base.position_at(0, 0.5)

                with BuildSketch( Plane(base).shift_origin(pos) ):
                    with Locations( *self.positions() ):
                        Rectangle(
                            self.config.divider, self.config.card.width,
                            align=(Align.MIN, Align.CENTER) )
                extrude(amount=self.config.height * 0.66)

        show(box, show_sketch_local=False)

        # TODO: add external walls
        self.parts.append(AutomatablePart(
            box.part, f"{self.config.name} card-box.stl",
            display_location=Location((0, 0, 0)),
            stl_folder=self.config.stl_folder,
        ))

    def is_sectioned(self):
        return len(self.config.sections) > 1

    def positions(self):
        return map(
            lambda pos: (pos, 0),
            accumulate(
                self.config.sections[1:-1],
                lambda x, y: x + y + self.config.divider,
                initial=self.config.sections[0]) )


if __name__ == "__main__":
    box = SectionedBox()
    box.compile()

    log.info("SectionedBox should be loaded")
