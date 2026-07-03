import yaml
import logging
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass

from ocp_vscode import show
from build123d import Align, Box, Compound, Pos, Rotation, Vector

from utils import prime
from location_box import LocationBox
from item_box import SectionedBox, SectionedBoxConfig


log = logging.getLogger(__name__)

GAP = 1.0
BUFFER = 0.1
LOC_ROW_COUNT = 11


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

def load_acts(path="src/acts.yaml") -> list[Act]:
    return load_yaml_as(Act, "acts", path)

def load_yaml_as(cls, key, path):
    doc = yaml.safe_load(Path(path).read_text())
    return [cls(name=name, **body) for name, body in doc[key].items()]

def load_boxes(path="src/boxes.yaml") -> list[RowBox]:
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
        while len(self.objects) < LOC_ROW_COUNT:
            corner = Vector(self._location_box_offset, GAP, BUFFER)
            self._location_box_offset += box.X + GAP
            box = (yield corner).bounding_box().size

        # the last box goes elsewhere
        yield self.standard_box_cursor(
            row=max(self._standard_box_offset),
            move_by=box.Y
        )

    def _loc_rotation(self, count):
        return Rotation(0, 0, 0 if count >= LOC_ROW_COUNT else 90)

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
    gamebox = GameBox(
        locations=load_locations(),
        standard_boxes=load_boxes(),
    )

    gamebox.render()
    log.info("gamebox rendered!")
