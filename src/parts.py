import os
from pathlib import Path

import build123d as bd
import partomatic as partz

from utils import WALL, compiled

REPO_ROOT = Path(os.environ["REPO_ROOT"])


class Partomatic(partz.Partomatic):
    @compiled
    def assembly(self):
        return bd.Compound(
            label=self.config.name,
            children=[p.part for p in self.parts]
        )

class Card(partz.PartomaticConfig):
    width: int
    height: int


class BaseConfig(partz.PartomaticConfig):
    color: str
    name: str


class CardboardConfig(BaseConfig):
    stl_folder: str = "NONE"

    # These need to be defined on subclasses
    width: float
    height: float
    depth: float

class Cardboard(Partomatic):
    config: CardboardConfig

    @property
    def stl_name(self):
        return self.config.name

    def compile(self):
        self.parts.clear()

        with bd.BuildPart() as board:
            bd.Box(self.config.width, self.config.depth, self.config.height)

        board.part.color = bd.Color(self.config.color)
        self.parts.append(partz.AutomatablePart(
            board.part, f"{self.stl_name}.stl",
            display_location=bd.Location((0, 0, 0)),
            stl_folder=self.config.stl_folder,
        ))

class BaseBoxConfig(BaseConfig):
    wall: float = WALL
    stl_folder: str = str(REPO_ROOT / "build")

class CardBoxConfig(BaseBoxConfig):
    # These need to be defined on subclasses
    card: Card

    @classmethod
    def footprint_width(cls):
        card = cls.__dataclass_fields__["card"].default_factory
        return cls._card_width_formula(card, cls.wall)

    @classmethod
    def footprint_height(cls):
        card = cls.__dataclass_fields__["card"].default_factory
        return card.height + cls.wall

    @staticmethod
    def _card_width_formula(card, wall):
        return card.width + (wall * 2)

    @property
    def face(self):
        return self._card_width_formula(self.card, self.wall)

    @property
    def depth(self):
        return self.inside_floor + (self.wall * 2)

    @property
    def height(self):
        return self.card.height + self.wall
