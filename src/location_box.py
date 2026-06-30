import logging
from dataclasses import field

from ocp_vscode import show, Animation

from build123d import *
from partomatic import AutomatablePart, PartomaticConfig

from parts import Partomatic, Card, CardBoxConfig
from utils import cshift, stack_thickness

FIT = 0.2
CENTERED = (Align.MAX, Align.CENTER)
log = logging.getLogger(__name__)


class Tarot(Card):
    width: int = 75
    height: int = 125

class Magnet(PartomaticConfig):
    diameter: float = 3
    thickness: float = 1

class LocationBoxConfig(CardBoxConfig):
    card: Card = field(default_factory=Tarot)
    magnet: Magnet = field(default_factory=Magnet)

    ##################################
    # Defaults are `tutorial`
    name: str = "tutorial"
    color: str = "green"
    card_count: int = 14

    @property
    def lid_length(self):
        return self.face - self.wall

    @property
    def inside_floor(self):
        return stack_thickness(self.card_count)

class LocationBox(Partomatic):
    config: LocationBoxConfig = LocationBoxConfig()

    fillet: float = 2.0
    lid_head: float = 5

    box_magnet_inset: float = -0.2   # a skin shy of the well
    lid_magnet_inset: float = -0.45

    @property
    def lid_inset(self):
        return self.lid_head / 2

    @property
    def box_params(self):
        return [
            self.config.face,
            self.config.depth,
            self.config.height + self.lid_head,
        ]

    def cut_magnet(self, face, inset):
        diameter = self.config.magnet.diameter + FIT
        depth = self.config.magnet.thickness + FIT

        top = face.edges().sort_by(Axis.Z)[-1].center()
        center = top - Vector(0, 0, self.lid_inset)
        pocket = Plane(face).shift_origin(center).offset(inset)

        return extrude(pocket * Rectangle(diameter, diameter), amount=-depth)

    def _shell(self):
        solid = Box(*self.box_params, align=(Align.MIN,) * 3)
        mouth = solid.faces().sort_by(Axis.Z)[-1]
        return offset(solid, amount=-self.config.wall, openings=mouth)

    def _lid_plane(self, shell):
        face = shell.faces().filter_by(Plane.YZ).sort_by(Axis.X)[-1]
        return Plane(face).shift_origin(face.position_at(1, 0.5))

    def _head(self, plane):
        profile = Rectangle(
            -self.lid_head, self.config.depth, align=CENTERED)
        return plane * profile

    def _lid_slot(self, plane):
        floor = self.config.inside_floor
        rail = Rectangle(-self.lid_head, floor, align=CENTERED)
        neck = Rectangle(
            -self.lid_inset, floor + self.config.wall, align=CENTERED)
        return plane * (rail + Pos(-self.lid_inset, 0) * neck)

    def _box(self, shell, plane, head, slot):
        wall = self.config.wall
        # remove the end of the key
        box = shell - extrude(head, amount=-wall)
        box -= extrude(slot, amount=-self.config.lid_length)

        back = box.faces().filter_by(Plane.YZ).sort_by(Axis.X)[1]
        box -= self.cut_magnet(back, self.box_magnet_inset)

        box = self._polish_box_edges(box)
        self._lock(box, plane)
        return box

    def _lid(self, plane, head, slot):
        length = self.config.lid_length
        rail = extrude(offset(slot, -FIT), amount=-length)
        cap = extrude(rail.faces().sort_by(Axis.Z)[-1], amount=FIT)
        lid = rail + cap + extrude(head, amount=-self.config.wall)

        tail = lid.faces().filter_by(Plane.YZ).sort_by(Axis.X)[0]
        lid -= self.cut_magnet(tail, self.lid_magnet_inset)

        lid = self._polish_lid_edges(lid)
        RigidJoint("key", to_part=lid, joint_location=Location(plane.origin))
        return lid

    def _lock(self, box, plane):
        LinearJoint(
            "lock", to_part=box,
            axis=Axis(plane.origin, plane.z_dir),
            linear_range=(0, self.config.lid_length))

    def _polish_box_edges(self, box):
        verticals = box.edges().filter_by(Axis.Z).group_by(Axis.X)
        top_bot = box.edges().filter_by(Plane.XY).group_by(Axis.Z)
        sides = top_bot[-1].filter_by(Axis.X).group_by(Axis.Y)
        ends = top_bot[-1].filter_by(Axis.Y).group_by(Axis.X)

        outer = verticals[0] + verticals[-1] + top_bot[0]
        rim = sides[0] + sides[-1] + ends[0]
        return fillet(outer + rim, self.fillet)

    def _polish_lid_edges(self, lid):
        verticals = lid.edges().filter_by(Axis.Z).group_by(Axis.X)[-1]
        top = lid.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1]
        sides = top.filter_by(Axis.X).group_by(Axis.Y)
        ends = top.filter_by(Axis.Y).group_by(Axis.X)

        # the lid's edge sits flush with the box itself
        flush = verticals + sides[0] + sides[-1] + ends[-1]
        return fillet(flush, self.fillet)

    def compile(self):
        self.parts.clear()

        shell = self._shell()
        plane = self._lid_plane(shell)
        head = self._head(plane)
        slot = self._lid_slot(plane)

        box = self._box(shell, plane, head, slot)
        lid = self._lid(plane, head, slot)

        box.joints["lock"].connect_to(lid.joints["key"], position=0)

        box.label = "box"
        box.color = Color(self.config.color)
        lid.label = "lid"
        lid.color = cshift(box.color)

        self.parts.append(AutomatablePart(
            box, f"{self.config.name} box.stl",
            display_location=Location((0, 0, 0)),
            stl_folder=self.config.stl_folder))
        self.parts.append(AutomatablePart(
            lid, f"{self.config.name} lid.stl",
            display_location=Location((0, 0, 0)),
            stl_folder=self.config.stl_folder))

if __name__ == "__main__":
    box = LocationBox()
    box.partomate()

    asm = box.assembly()
    show(asm, render_joints=True)

    slide = box.config.lid_length + 10
    anim = Animation()
    anim.add_track(
        f"/{box.config.name}/lid",
        "tx",
        times=[0, 1, 2],
        values=[0, slide, 0] )
    anim.animate(speed=0.9)

    log.info("processed location_box")
