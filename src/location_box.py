import logging
from dataclasses import field

from ocp_vscode import show, Animation

from build123d import *
from partomatic import AutomatablePart, PartomaticConfig

from parts import Partomatic, Card, CardBoxConfig
from utils import cshift, stack_thickness


log = logging.getLogger(__name__)

FIT = 0.2
CENTERED = (Align.MAX, Align.CENTER)


class Tarot(Card):
    width: int = 75
    height: int = 125

class Magnet(PartomaticConfig):
    diameter: float = 3
    thickness: float = 1

class LocationBoxConfig(CardBoxConfig):
    card: Tarot = field(default_factory=Tarot)
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

    @property
    def lid_inset(self):
        return self.lid_head / 2

    @property
    def box_params(self):
        return [
            self.config.face,
            self.config.depth,
            self.config.height + self.lid_head
        ]

    def compile(self):
        self.parts.clear()

        with BuildPart() as box:
            self._build_shell()

            lid_plane = self._lid_plane()
            self._cut_lid_rail(lid_plane)

            box_mag_face = faces().filter_by(Plane.YZ).sort_by(Axis.X)[1]
            self.cut_magnet(box_mag_face)

            self._fillet_box()

        with BuildPart() as lid:
            self._build_lid(lid_plane)
            RigidJoint("key", joint_location=Location(lid_plane.origin) )

            lid_mag_face = faces().filter_by(Plane.YZ).sort_by(Axis.X)[0]
            self.cut_magnet(lid_mag_face)

            self._fillet_lid()

        # Connect the lid as a joint
        box.part.joints["lock"].connect_to( lid.part.joints["key"], position=0 )

        # Set colors
        box.part.label = "box"
        box.part.color = Color(self.config.color)

        lid.part.label = "lid"
        lid.part.color = cshift(box.part.color)

        self.parts.append(AutomatablePart(
            box.part, f"{self.config.name} box.stl",
            display_location=Location((0, 0, 0)),
            stl_folder=self.config.stl_folder,
        ))

        self.parts.append(AutomatablePart(
            lid.part, f"{self.config.name} lid.stl",
            display_location=Location((0, 0, 0)),
            stl_folder=self.config.stl_folder,
        ))

    def _build_shell(self):
        Box(*self.box_params, align=(Align.MIN, Align.MIN, Align.MIN))
        offset(amount=-self.config.wall, openings=faces().sort_by(Axis.Z)[-1])

    def _lid_plane(self):
        face = faces().filter_by(Plane.YZ).sort_by(Axis.X)[-1]
        return Plane(face).shift_origin(face.position_at(1, 0.5))

    def _cut_lid_rail(self, plane):
        # remove the end of the key
        extrude(
            self.head_profile(plane),
            amount=-self.config.wall,
            mode=Mode.SUBTRACT )

        #  now we need to cut the small keyhole groove (the slide joint)
        add(self.key(plane), mode=Mode.SUBTRACT)

        LinearJoint(
            "lock",
            axis=Axis(plane.origin, plane.z_dir),
            linear_range=(0, self.config.lid_length),
        )

    def key(self, plane):
        profile = self.key_profile(plane)
        return extrude(
            profile, amount=-self.config.lid_length, mode=Mode.PRIVATE )

    def key_profile(self, plane):
        with BuildSketch(plane) as key:
            Rectangle(
                -self.lid_head, self.config.inside_floor, align=CENTERED)
            with Locations((-self.lid_inset, 0)):
                Rectangle(
                    -self.lid_inset,
                    self.config.inside_floor + self.config.wall,
                    align=CENTERED,
                )

        return key.sketch

    def cut_magnet(self, face):
        diameter, depth = map(lambda x: x + FIT, [
            self.config.magnet.diameter,
            self.config.magnet.thickness,
        ])

        top = face.edges().sort_by(Axis.Z)[-1].center()
        magnet_center = top - Vector(0, 0, (self.lid_head - FIT) / 2)
        plane = Plane(face).shift_origin(magnet_center)

        with BuildSketch(plane) as magnet:
            Circle( (diameter + FIT ) / 2)

        extrude(magnet.sketch, amount=-depth, mode=Mode.SUBTRACT)

    def _fillet_box(self):
        verticals = edges().filter_by(Axis.Z).group_by(Axis.X)

        top_bot = edges().filter_by(Plane.XY).group_by(Axis.Z)
        sides   = top_bot[-1].filter_by(Axis.X).group_by(Axis.Y)
        ends    = top_bot[-1].filter_by(Axis.Y).group_by(Axis.X)

        # outer four edges and the bottom
        box_edges = verticals[0] + verticals[-1] + top_bot[0]

        # the top outer 3 edges
        box_edges += sides[0] + sides[-1] + ends[0]
        fillet(box_edges, self.fillet)

    def _build_lid(self, plane):
        add( offset( self.key(plane), -FIT,
            kind=Kind.INTERSECTION, mode=Mode.PRIVATE) )
        extrude(faces().sort_by(Axis.Z)[-1], amount=FIT)
        extrude(self.head_profile(plane), amount=-self.config.wall)

        bottom = faces().sort_by(Axis.Z)[0]
        extrude(bottom, amount=-FIT, mode=Mode.SUBTRACT)

    def _fillet_lid(self):
        verticals = edges().filter_by(Axis.Z).group_by(Axis.X)[-1]

        top   = edges().filter_by(Plane.XY).group_by(Axis.Z)[-1]
        sides = top.filter_by(Axis.X).group_by(Axis.Y)
        ends  = top.filter_by(Axis.Y).group_by(Axis.X)

        # we want the lid's edge to sit flush with the box itself
        fillet(verticals + sides[0] + sides[-1] + ends[-1], self.fillet)

    def head_profile(self, plane):
        with BuildSketch(plane) as head:
            Rectangle(-self.lid_head, self.config.depth, align=CENTERED)

        return head.sketch

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
