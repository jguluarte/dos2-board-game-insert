import yaml
import logging
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass

from ocp_vscode import show
from build123d import Align, Box, Compound, Pos, Rotation, Vector

from parts import REPO_ROOT
from utils import prime
from location_box import LocationBox
from item_box import SectionedBox, SectionedBoxConfig


log = logging.getLogger(__name__)

GAP = 1.0
BUFFER = 0.1
LOCATION_ROW_CAPACITY = 10

def is_in_location_row(n):
    return n < LOCATION_ROW_CAPACITY


@dataclass
class Act:
    name: str
    color: str
    card_stacks: list[int]

@dataclass
class RowBox:
    row: int
    box: SectionedBox

def load_locations() -> list[LocationBox]:
    return [
        LocationBox(name=act.name, color=act.color, card_count=stack)
        for act in load_acts() for stack in act.card_stacks]

def load_acts(path=REPO_ROOT / "data/acts.yaml") -> list[Act]:
    return load_yaml_as(Act, "acts", path)

def load_yaml_as(cls, key, path):
    doc = yaml.safe_load(Path(path).read_text())
    return [cls(name=name, **body) for name, body in doc[key].items()]

def load_boxes(path=REPO_ROOT / "data/boxes.yaml") -> list[RowBox]:
    doc = yaml.safe_load(Path(path).read_text())
    return [
        RowBox(row, SectionedBox(name=name, **body))
        for row, entries in enumerate(doc["standard_boxes"])
        for name, body in entries.items()]

def place_at(obj, point):
    return Pos(point - obj.bounding_box().min) * obj

class GameBox:
    # static constants
    width: int = 395
    depth: int = 303
    height: int = 175

    def __init__(self, locations, standard_boxes):
        self.objects = []

        back = self.depth - GAP
        self._location_box_offset = GAP
        self._standard_box_offset = {r.row: back for r in standard_boxes}

        # locations must go first
        self.place_locations(locations)
        self.place_boxes(standard_boxes)

    def place_locations(self, locations):
        cursor = self.gen_location_corner()

        for i, loc in enumerate(locations):
            box = self._loc_rotation(i) * loc.assembly()
            self.objects.append( place_at(box, cursor.send(box)) )

    @prime
    def gen_location_corner(self):
        box = (yield).bounding_box().size

        # things that fit in the main row
        while is_in_location_row(len(self.objects)):
            corner = Vector(self._location_box_offset, GAP, BUFFER)
            self._location_box_offset += box.X + GAP
            box = (yield corner).bounding_box().size

        # the boxes that don't fit consume standard-row slots
        while True:
            box = (yield self.standard_box_cursor(
                row=max(self._standard_box_offset),
                move_by=box.Y,
            )).bounding_box().size

    def _loc_rotation(self, count):
        return Rotation(0, 0, 90 if is_in_location_row(count) else 0)

    def place_boxes(self, row_boxes):
        for r in row_boxes:
            part = Rotation(0, 0, 90) * r.box.assembly()
            box = part.bounding_box().size

            self.objects.append( place_at(
                part, self.standard_box_cursor(row=r.row, move_by=box.Y)
            ))

    def standard_box_cursor(self, row, move_by) -> Vector:
        std_row_width = SectionedBoxConfig.footprint_width() + GAP

        # (x, y) coords
        pos_row = row * std_row_width + GAP
        pos_box = self._standard_box_offset[row] - move_by

        # Move inward from the back of the box
        self._standard_box_offset[row] = pos_box - GAP

        return Vector(pos_row, pos_box, BUFFER)

    def render(self):
        show(*self.objects, self.wireframe())

    def wireframe(self):
        interior = Box(
            self.width, self.depth, self.height,
            align=(Align.MIN, Align.MIN, Align.MIN) )

        return Compound( children=interior.edges() )


if __name__ == "__main__":

    for b in (std_boxes := load_boxes()):
        if b.box.config.name in ("items", "characters"):
            b.box.partomate()

    gamebox = GameBox(
        locations=load_locations(),
        standard_boxes=std_boxes,
    )

    gamebox.render()
    log.info("gamebox rendered!")
