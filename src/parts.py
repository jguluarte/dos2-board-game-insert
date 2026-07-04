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

class CardBoxConfig(partz.PartomaticConfig):
    wall: float = WALL
    stl_folder: str = str(REPO_ROOT / "build")

    # These need to be defined on subclasses
    card: Card
    name: str

    @classmethod
    def footprint_width(cls):
        card = cls.__dataclass_fields__["card"].default_factory
        return cls._card_width_formula(card, cls.wall)

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
