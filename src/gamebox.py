import yaml
import logging
from pathlib import Path
from itertools import chain
from dataclasses import dataclass

from ocp_vscode import show
from build123d import Align, Box, Compound, Pos, Rotation, Vector

from parts import REPO_ROOT
from utils import prime
from location_box import LocationBox
from item_box import SectionedBox, SectionedBoxConfig
from cardboard import (
    BossDeck, BossTracker, HallOfEchoes, Minion, Player, RoundTracker)
from status import StatusBox


log = logging.getLogger(__name__)

GAP = 1.0
BUFFER = 0.1
LOCATION_ROW_CAPACITY = 10
STD_ROW = SectionedBoxConfig.footprint_width() + GAP

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
        LocationBox(name=f"{act.name}-{i}", color=act.color, card_count=stack)
        for act in load_acts()
        for i, stack in enumerate(act.card_stacks, start=1)]

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
    width: int = 395
    depth: int = 303
    height: int = 175

    # known properties of the game
    hall = HallOfEchoes()
    tracker = RoundTracker()
    status_tray = StatusBox()
    minions = [Minion(name=n) for n in "abcdef"]
    players = [Player(name=n) for n in ["one", "two", "three", "four"]]

    boss_deck = BossDeck()
    boss_tracker = BossTracker()

    @property
    def BACK(self) -> Vector:
        return Vector(self.width - GAP, self.depth - GAP, self.height - GAP)

    def __init__(self, locations, standard_boxes):
        self._raw_boxes = [
            i for i in chain(locations, [a.box for a in standard_boxes]) ]

        self.locations = []
        self.game_pieces = []
        self.standard_boxes = []
        self._status_tray = None

        self._location_box_offset = GAP
        self._standard_box_offset = {r.row: GAP for r in standard_boxes}

        self.place_standard_boxes(standard_boxes)
        self.place_locations(locations)
        self.place_status_tray()
        self.place_game_pieces()

    def place_standard_boxes(self, row_boxes):
        # the rows march from the back corner
        for r in row_boxes[:-1]:
            part = r.box.assembly()
            box = part.bounding_box().size

            self.standard_boxes.append( place_at(
                part, self.standard_box_cursor(row=r.row, move_by=box.X)
            ))

        # Last box has unique placement
        box = row_boxes[-1].box.assembly()
        self.standard_boxes.append( place_at(box, Vector(
            self.status_tray.config.width + GAP * 2,
            self.location_row_gap(), BUFFER) ))

    def standard_box_cursor(self, row, move_by) -> Vector:
        pos_box = self._standard_box_offset[row]
        pos_row = self.BACK.Y - (row + 1) * STD_ROW + GAP

        # move cursor rightward
        self._standard_box_offset[row] = pos_box + move_by + GAP
        return Vector(pos_box, pos_row, BUFFER)

    def location_row_gap(self) -> float:
        # the Y line where the gap behind the location row begins
        return self.BACK.Y - STD_ROW * 3 + GAP

    def place_locations(self, locations):
        cursor = self.gen_location_corner()

        for loc in locations[:LOCATION_ROW_CAPACITY]:
            box = Rotation(0, 0, 90) * loc.assembly()
            self.locations.append( place_at(box, cursor.send(box)) )

        # the last few locations have bespoke handling
        for loc in locations[LOCATION_ROW_CAPACITY:]:
            box = loc.assembly()
            self.locations.append( place_at(box, cursor.send(box)) )

    @prime
    def gen_location_corner(self):
        box = (yield).bounding_box().size

        # the main row, growing along the front wall
        while is_in_location_row(len(self.locations)):
            corner = Vector(self._location_box_offset, GAP, BUFFER)
            self._location_box_offset += box.X + GAP
            box = (yield corner).bounding_box().size

        # put the last couple locations at the end of the box
        edge = self.location_row_gap()
        while True:
            corner = Vector(self.BACK.X - box.X - 7, edge, BUFFER)
            edge += box.Y + GAP
            box = (yield corner).bounding_box().size

    def place_status_tray(self):
        tray = self.status_tray.assembly()

        self._status_tray = place_at(
            tray, Vector(GAP, self.location_row_gap(), BUFFER) )

    def place_game_pieces(self):
        self.place_boss_components()
        self.place_minions()
        self.place_hall()
        self.stack_boards()

    def place_boss_components(self):
        pieces = []

        #######################
        # boss tracker
        tracker = Rotation(0, 0, 90) * self.boss_tracker.assembly()
        pos_x = tracker.bounding_box().size.X

        pieces.append( place_at(
            tracker, Vector(self.BACK.X - pos_x, GAP, BUFFER) ))

        #######################
        # boss discard
        discard = Rotation(90, 0, 90) * self.boss_deck.assembly()
        size = discard.bounding_box().size

        pieces.append( place_at(discard, Vector(
            self.BACK.X - 4 - size.X, self.BACK.Y - size.Y, BUFFER) ))

        self.game_pieces.append( Compound(label="Boss", children=pieces) )

    def place_minions(self):
        minions = []
        edge = self.BACK.X - 7  # inset next to other things

        for m in self.minions:
            board = Rotation(90, 0, 90) * m.assembly()
            size = board.bounding_box().size
            edge -= size.X
            minions.append( place_at(
                board, Vector(edge, self.BACK.Y - size.Y, BUFFER) ))

        self.game_pieces.append( Compound(label="minions", children=minions) )

    def place_hall(self):
        book = Rotation(0, 90, 0) * self.hall.assembly()
        size = book.bounding_box().size

        self.game_pieces.append( place_at(book, Vector(
            GAP, self.BACK.Y - STD_ROW * 2 - size.Y, BUFFER) ))

    def stack_boards(self):
        roof = SectionedBoxConfig.footprint_height() + BUFFER
        boards = []

        for b in [self.tracker, *self.players]:
            board = Rotation(90, 0, 0) * b.assembly()
            size = board.bounding_box().size
            boards.append( place_at(
                board, Vector(GAP, self.BACK.Y - size.Y, roof) ))
            roof += size.Z

        self.game_pieces.append( Compound(
            label="player & round", children=boards ))


    def render(self):
        show(
            self.locations, self.standard_boxes, self._status_tray,
            self.game_pieces, self.wireframe(),
            names=[
                "locations", "standard boxes", "status tray",
                "game pieces", "wireframe"],
        )

    def wireframe(self):
        interior = Box(
            self.width, self.depth, self.height,
            align=(Align.MIN, Align.MIN, Align.MIN) )

        return Compound( label="wireframe", children=interior.edges() )

    def partomate(self):
        for i in (*self._raw_boxes, self.status_tray):
            i.partomate()


if __name__ == "__main__":
    gamebox = GameBox(
        locations=load_locations(),
        standard_boxes=load_boxes(),
    )

    gamebox.render()
    log.info("gamebox rendered!")

    gamebox.partomate()
    log.info("gamebox partomated bruhv")
