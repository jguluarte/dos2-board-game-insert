import yaml
import logging
from pathlib import Path
from dataclasses import dataclass

from ocp_vscode import show
from build123d import Align, Box, Compound, Pos, Rotation, Vector

from parts import REPO_ROOT
from utils import prime
from location_box import LocationBox
from item_box import SectionedBox, SectionedBoxConfig
from cardboard import (
    BossDeck, BossTracker, HallOfEchoes, Minion, Player, RoundTracker)


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

    # known properties of the game
    hall = HallOfEchoes()
    tracker = RoundTracker()
    players = [Player(name=n) for n in ["one", "two", "three", "four"]]
    minions = [Minion(name=n) for n in "abcdef"]
    boss_tracker = BossTracker()
    boss_deck = BossDeck()

    @property
    def BACK(self) -> Vector:
        return Vector(self.width - GAP, self.depth - GAP, self.height - GAP)

    def __init__(self, locations, standard_boxes):
        # catchall
        self.objects = []

        self.locations = []
        self.standard_boxes = []

        self._location_box_offset = GAP
        self._standard_box_offset = {r.row: self.BACK.Y for r in standard_boxes}

        # Sequencing matters. We'll build on things as we go.
        # locations are hard coded and very specific. if it changes, we know.
        self.place_locations(locations[:LOCATION_ROW_CAPACITY])
        self.place_boxes(standard_boxes)
        self.place_tutorial(locations[-1])
        self.place_nemesis(locations[-2])
        self.place_boss_tracker(self.boss_tracker)
        self.place_minions(self.minions)
        self.place_boss_deck(self.boss_deck)
        self.place_hall(self.hall)
        self.stack_boards([self.tracker, *self.players])

    def place_locations(self, locations):
        cursor = self.gen_location_corner()

        for loc in locations:
            box = Rotation(0, 0, 90) * loc.assembly()
            self.locations.append( place_at(box, cursor.send(box)) )

    @prime
    def gen_location_corner(self):
        box = (yield).bounding_box().size

        # things that fit in the main row
        while is_in_location_row(len(self.locations)):
            corner = Vector(self._location_box_offset, GAP, BUFFER)
            self._location_box_offset += box.X + GAP
            box = (yield corner).bounding_box().size

    def place_boxes(self, row_boxes):
        for r in row_boxes:
            part = Rotation(0, 0, 90) * r.box.assembly()
            box = part.bounding_box().size

            self.standard_boxes.append( place_at(
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

    def place_tutorial(self, tutorial):
        # aligned in front of its card box, so the tutorial pieces cluster
        sibling = self.standard_boxes[-1].bounding_box()
        box = tutorial.assembly()
        depth = box.bounding_box().size.Y

        self.locations.append( place_at(
            box, Vector(sibling.min.X, sibling.min.Y - GAP - depth, BUFFER) ))

    def place_nemesis(self, nemesis):
        # tucked in front of the tutorial cluster
        neighbor = self.locations[-1].bounding_box()
        box = nemesis.assembly()
        depth = box.bounding_box().size.Y

        self.locations.append( place_at(box, Vector(
            neighbor.min.X, neighbor.min.Y - GAP - depth, BUFFER) ))

    def place_boss_tracker(self, tracker):
        # standing against the wall, running the length of the box
        board = Rotation(0, 0, 90) * tracker.assembly()
        size = board.bounding_box().size

        self.objects.append( place_at(
            board, Vector(self.BACK.X - size.X, GAP, BUFFER) ))

    def place_minions(self, minions):
        # standing behind the row, leaning on the boss tracker
        boss = self.objects[0].bounding_box()
        edge = self.locations[0].bounding_box().max.Y + GAP

        for m in minions:
            board = Rotation(0, 90, 0) * m.assembly()
            size = board.bounding_box().size
            self.objects.append( place_at(
                board, Vector(boss.min.X - size.X, edge, BUFFER) ))
            edge += size.Y

    def place_boss_deck(self, deck):
        # standing in the sliver between the boxes and the envelope
        board = Rotation(90, 0, 90) * deck.assembly()
        size = board.bounding_box().size
        sliver = max(b.bounding_box().max.X for b in self.standard_boxes)

        self.objects.append( place_at(board, Vector(
            sliver + GAP, self.BACK.Y - size.Y, BUFFER) ))

    def place_hall(self, hall):
        # the squishy envelope stands in the sliver, leaning on the boss tracker
        book = Rotation(90, 0, 90) * hall.assembly()
        size = book.bounding_box().size
        boss = self.objects[0].bounding_box()

        self.objects.append( place_at(book, Vector(
            boss.min.X - size.X, self.BACK.Y - size.Y, BUFFER) ))

    def stack_boards(self, boards):
        roof = self.standard_boxes[0].bounding_box().max.Z

        for b in boards:
            board = Rotation(90, 0, 0) * b.assembly()
            size = board.bounding_box().size
            self.objects.append( place_at(
                board, Vector(GAP, self.BACK.Y - size.Y, roof) ))
            roof += size.Z

    def render(self):
        show(
            self.locations, self.standard_boxes, self.objects, self.wireframe(),
            names=["locations", "standard boxes", "game pieces", "wireframe"],
        )

    def wireframe(self):
        interior = Box(
            self.width, self.depth, self.height,
            align=(Align.MIN, Align.MIN, Align.MIN) )

        return Compound( label="wireframe", children=interior.edges() )


if __name__ == "__main__":

    for b in (std_boxes := load_boxes()):
        if b.box.config.name not in ("tutorial", "minions", "bosses"):
            b.box.partomate()

    gamebox = GameBox(
        locations=load_locations(),
        standard_boxes=std_boxes,
    )

    gamebox.render()
    log.info("gamebox rendered!")
