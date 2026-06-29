import logging
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from build123d import Align, Box, Compound, Pos, Rotation, Vector

from location_box import LocationBox
from utils import prime


log = logging.getLogger(__name__)

GAP = 1.0
BUFFER = 0.1


@dataclass
class Act:
    name: str
    color: str
    card_stacks: list[int]

def load_locations() -> list[LocationBox]:
    return [
        LocationBox(name=act.name, color=act.color, card_count=stack)
        for act in load_acts() for stack in act.card_stacks]

def load_acts(path="src/acts.yaml") -> list[Act]:
    doc = yaml.safe_load(Path(path).read_text())
    return [Act(name=name, **body) for name, body in doc["acts"].items()]

def place_at(obj, point):
    return Pos(point - obj.bounding_box().min) * obj

class GameBox:
    # static constants
    width: int = 395
    depth: int = 303
    height: int = 175

    def __init__(self):
        self.locations = []
        self._location_offset = GAP

        self.loc_cursor = self.gen_location_corner()

    def add_location(self, location):
        box = Rotation(0, 0, 90) * location.assembly()

        cursor = self.loc_cursor.send(box)
        self.locations.append( place_at(box, cursor) )

    @prime
    def gen_location_corner(self):
        box = (yield).bounding_box().size

        # things that fit in the main row
        while len(self.locations) < 11:
            corner = Vector(self._location_offset, GAP, BUFFER)
            self._location_offset += box.X + GAP
            box = (yield corner).bounding_box().size

        # the final straggler
        yield Vector(
            self.width - GAP - box.X,
            self.depth - GAP - box.Y,
            BUFFER
        )

    def render(self):
        from ocp_vscode import show
        show(*self.locations, self.wireframe())

    def wireframe(self):
        interior = Box(
            self.width, self.depth, self.height,
            align=(Align.MIN, Align.MIN, Align.MIN) )

        return Compound( children=interior.edges() )


if __name__ == "__main__":
    gamebox = GameBox()

    for box in load_locations():
        gamebox.add_location(box)

    gamebox.render()
    log.info("gamebox rendered!")
