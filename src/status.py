from contextlib import contextmanager
import logging
from dataclasses import field

from ocp_vscode import show

from build123d import *
from partomatic import AutomatablePart

from utils import stack_thickness
from parts import Partomatic, Card, BaseBoxConfig

from cardboard import MinionConfig


log = logging.getLogger(__name__)

# yeah the numbers don't match the var name
# this is to give a bit of extra flex room inside the boxes
SIX = stack_thickness(8)
ELEVEN = stack_thickness(13)

MIN_MIN = (Align.MIN, Align.MIN)

MINION_DEPTH = 7
MINION_WIDTH = MinionConfig.width + 2


class Mini(Card):
    width: float = 44
    height: float = 66

class StatusBoxConfig(BaseBoxConfig):
    name: str = "status-tray"
    color: str = "steelblue"
    card: Mini = field(default_factory=Mini)

    pockets: int = 5
    divider: float = 1.2
    fillet: float = 1.0

    @property
    def card_sections(self):
        return [SIX, ELEVEN, ELEVEN]

    @property
    def width(self) -> float:
        outer_wall = self.wall * 2
        inner_wall = self.divider * (self.pockets - 1)

        return (self.card.width * self.pockets) + outer_wall + inner_wall

    @property
    def inset(self):
        return self.card.height / 2

    @property
    def grid_width(self) -> float:
        return self.card.width + self.divider


class StatusBox(Partomatic):
    config: StatusBoxConfig = StatusBoxConfig()

    def compile(self):
        self.parts.clear()

        with BuildPart() as box:
            for i, stack in enumerate(self.config.card_sections, start=1):
                with Locations(( 0, self._grid_offset(i) )):
                    self._add_status_row(i, stack)

            with Locations(( 0, self._grid_offset(4) + self.config.divider )):
                self._add_minion_slots()

            self._fillet_shell()

        box.part.color = Color("maroon")
        self.parts.append(AutomatablePart(
            box.part, "status.stl",
            stl_folder=self.config.stl_folder,
        ))

    def _fillet_shell(self):
        # one continuous pass over the outer shell; pocket/minion wells stay sharp
        verticals = edges().filter_by(Axis.Z).group_by(Axis.X)
        outer_vert = verticals[0] + verticals[-1]

        horiz = edges().filter_by(Plane.XY)
        bottom = horiz.group_by(Axis.Z)[0]                   # base perimeter

        # full-width front lip of each rising step + the top-plane back edge
        railings = horiz.filter_by(Axis.X).filter_by(
            lambda e: e.length > self.config.width / 2)

        # left/right side rail of every step ledge (and the top plane)
        sides = horiz.filter_by(Axis.Y).group_by(Axis.X)
        outer_sides = sides[0] + sides[-1]

        fillet(
            outer_vert + bottom + railings + outer_sides,
            radius=self.config.fillet)

    def _grid_offset(self, level):
        _lvl = level - 1

        # remove `* 2` when I want walls to overlap
        return _lvl * (self.config.divider * 1) + sum(
            self.config.card_sections[:_lvl])

    def _add_status_row(self, level, stack):
        depth = stack + (self.config.wall * 2)
        height = self._height_for_level(level)

        Box(self.config.width, depth, height, align=MIN_MIN)

        with self._status_grid() as s:
            Rectangle(self.config.card.width, stack)
        extrude(s.sketch, amount=-self.config.inset, mode=Mode.SUBTRACT)

    def _height_for_level(self, level) -> float:
        return level * self.config.inset + self.config.wall

    @contextmanager
    def _status_grid(self):
        cfg = self.config
        top_face = faces(Select.LAST).filter_by(Plane.top).sort_by(Axis.Z)[-1]

        with BuildSketch( top_face ) as s:
            with GridLocations(cfg.grid_width, cfg.wall, cfg.pockets, 1):
                yield s

    def _add_minion_slots(self):
        depth = (
            MINION_DEPTH * 3
            + (self.config.divider * 2)
            + (self.config.wall * 2) )

        height = self._height_for_level(3)

        b = Box(self.config.width, depth, height, align=MIN_MIN)
        top = b.faces().sort_by(Axis.Z)[-1]

        with self._minion_grid(top) as s:
            Rectangle(MINION_WIDTH, MINION_DEPTH)
        extrude(s.sketch, amount=-75, mode=Mode.SUBTRACT)

    @contextmanager
    def _minion_grid(self, top_face):
        cfg = self.config

        with BuildSketch( top_face ) as s:
            with GridLocations(
                    MINION_WIDTH + 20, MINION_DEPTH + cfg.divider, 2, 3):
                yield s



if __name__ == "__main__":
    box = StatusBox()
    box.compile()
    box.partomate()
    show(box.assembly(), show_sketch_local=False)

    log.info("status tray rendered")
    log.info(f"    inset ({box.config.inset})")
