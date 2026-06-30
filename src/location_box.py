import logging
from dataclasses import field

from ocp_vscode import show, Animation

from build123d import *
from partomatic import AutomatablePart, PartomaticConfig

from parts import Partomatic, Card, CardBoxConfig
from utils import cshift, stack_thickness

FIT = 0.2
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
    def stack(self):
        return stack_thickness(self.card_count)

    @property
    def depth(self):
        return self.stack + (self.wall * 2)

class LocationBox(Partomatic):
    config: LocationBoxConfig = LocationBoxConfig()

    fillet: float = 2.0
    lid_head: float = 5

    @property
    def lid_inset(self):
        return self.lid_head / 2

    @property
    def coords(self):
        return [
            self.config.face,
            self.config.depth,
            self.config.height + self.lid_head
        ]

    def cut_magnet(self, face, offset):
        diameter, depth = map(lambda x: x + FIT, [
            self.config.magnet.diameter,
            self.config.magnet.thickness,
        ])

        top = face.edges().sort_by(Axis.Z)[-1].center()
        magnet_center = top - Vector(0, 0, self.lid_inset)
        plane = Plane(face).shift_origin(magnet_center).offset(offset)

        with BuildSketch(plane) as magnet:
            Rectangle(diameter, diameter)

        extrude(magnet.sketch, amount=-depth, mode=Mode.SUBTRACT)

    def compile(self):
        self.parts.clear()

        centered = (Align.MAX, Align.CENTER)

        with BuildPart() as box:
            # Make the box & hollow it out
            Box(*self.coords, align=(Align.MIN, Align.MIN, Align.MIN))
            offset(
                amount=-self.config.wall,
                openings=faces().sort_by(Axis.Z)[-1] )

            # select the face to cut the lid out from, origin at its top center
            face = faces().filter_by(Plane.YZ).sort_by(Axis.X)[-1]
            lid_plane = Plane(face).shift_origin(face.position_at(1, 0.5))

            # remove the end of the key
            with BuildSketch(lid_plane) as head:
                Rectangle(-self.lid_head, self.config.depth, align=centered)

            extrude(amount=-self.config.wall, mode=Mode.SUBTRACT)

            #  now we need to cut the small keyhole groove (the slide joint)
            with BuildSketch(lid_plane) as lid_key:
                Rectangle(-self.lid_head, self.config.stack, align=centered)
                with Locations((-self.lid_inset, 0)):
                    Rectangle(
                        -self.lid_inset,
                        self.config.stack + self.config.wall,
                        align=centered,
                    )
            extrude(amount=-self.config.lid_length, mode=Mode.SUBTRACT)

            # magnet pocket cut into the back wall, a skin shy of the well
            back = faces().filter_by(Plane.YZ).sort_by(Axis.X)[1]
            self.cut_magnet(back, -0.2)

            ####################
            # Polish the edges
            verticals = edges().filter_by(Axis.Z).group_by(Axis.X)

            top_bot = edges().filter_by(Plane.XY).group_by(Axis.Z)
            sides   = top_bot[-1].filter_by(Axis.X).group_by(Axis.Y)
            ends    = top_bot[-1].filter_by(Axis.Y).group_by(Axis.X)

            # outer four edges and the bottom
            box_edges = verticals[0] + verticals[-1] + top_bot[0]

            # the top outer 3 edges
            box_edges += sides[0] + sides[-1] + ends[0]
            fillet(box_edges, self.fillet)

            LinearJoint(
                "lock",
                axis=Axis(lid_plane.origin, lid_plane.z_dir),
                linear_range=(0, self.config.lid_length),
            )

        with BuildPart() as lid:
            extrude(
                offset(lid_key.sketch, -FIT),
                amount=-self.config.lid_length )
            extrude(faces().sort_by(Axis.Z)[-1], amount=FIT)
            extrude(head.sketch, amount=-self.config.wall)

            # matching magnet pocket in the lid tail, facing the box magnet
            tail = faces().filter_by(Plane.YZ).sort_by(Axis.X)[0]
            self.cut_magnet(tail, -0.45)

            ####################
            # Polish the edges
            verticals = edges().filter_by(Axis.Z).group_by(Axis.X)[-1]

            top   = edges().filter_by(Plane.XY).group_by(Axis.Z)[-1]
            sides = top.filter_by(Axis.X).group_by(Axis.Y)
            ends  = top.filter_by(Axis.Y).group_by(Axis.X)

            # we want the lid's edge to sit flush with the box itself
            lid_edges = verticals + sides[0] + sides[-1] + ends[-1]
            fillet(lid_edges, self.fillet)

            RigidJoint("key", joint_location=Location(lid_plane.origin) )

        # Connect the lid as a joint
        box.part.joints["lock"].connect_to(
            lid.part.joints["key"], position=0)

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
