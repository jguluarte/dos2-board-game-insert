import build123d as bd
import partomatic as partz

from utils import stack_thickness, WALL, compiled, cshift


class Partomatic(partz.Partomatic):
    @compiled
    def assembly(self):
        return bd.Compound(
            label=self.config.name,
            children=[p.part for p in self.parts]
        )
