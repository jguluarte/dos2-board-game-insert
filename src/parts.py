import build123d as bd
import partomatic as partz

from utils import WALL, compiled


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
    stl_folder: str = "build"

    # These need to be defined on subclasses
    card: Card
    name: str

    @property
    def face(self):
        return self.card.width + (self.wall * 2)

    @property
    def height(self):
        return self.card.height + self.wall
