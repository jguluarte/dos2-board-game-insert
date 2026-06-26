import logging
from dataclasses import field

from build123d import *
from partomatic import AutomatablePart, Partomatic, PartomaticConfig

from utils import stack_thickness, WALL

log = logging.getLogger(__name__)

class Tarot(PartomaticConfig):
    width: int = 75
    height: int = 125

class LocationBoxConfig(PartomaticConfig):
    wall: float = WALL
    stl_folder: str = "build"
    card: Tarot = field(default_factory=Tarot)


    ##################################
    # Stubbed with `tutorial` values
    name: str = "tutorial"
    color: str = "gold"
    card_count: int = 14
    ##################################

    @property
    def depth(self):
        return stack_thickness(self.card_count)

    @property
    def face(self):
        return self.card.width

    # This is where I'll want to add height for the lid
    @property
    def height(self):
        return self.card.height


class LocationBox(Partomatic):
    config: LocationBoxConfig = LocationBoxConfig()

    def compile(self):
        self.parts.clear()
        self.parts.append(AutomatablePart(self.box(), "location"))

    def box(self):
        with BuildPart() as box:
            Box(self.config.face, self.config.depth, self.config.height)
            offset(amount=self.config.wall, openings=box.faces().sort_by(Axis.Z)[-1])

        box.part.color = Color(self.config.color)
        return box.part

    def assembly(self):
        self.compile()
        return Compound(children=[part.part for part in self.parts])


if __name__ == "__main__":
    from ocp_vscode import show

    box = LocationBox()
    box.compile()
    show(*(part.part for part in box.parts))

    log.info("processed location_box")
