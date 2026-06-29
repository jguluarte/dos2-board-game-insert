import logging
from dataclasses import field

from build123d import *
from partomatic import AutomatablePart, Partomatic, PartomaticConfig

from utils import stack_thickness, WALL, compiled, max_fillet, cshift

log = logging.getLogger(__name__)

FIT = 0.1

class Tarot(PartomaticConfig):
    width: int = 75
    height: int = 125

class Magnet(PartomaticConfig):
    diameter: float = 3
    thickness: float = 1

class LocationBoxConfig(PartomaticConfig):
    wall: float = WALL
    stl_folder: str = "build"
    card: Tarot = field(default_factory=Tarot)
    magnet: Magnet = field(default_factory=Magnet)


    ##################################
    # Stubbed with `tutorial` values
    name: str = "tutorial"
    color: str = "green"
    card_count: int = 14
    ##################################

    @property
    def depth(self):
        return self.stack + (self.wall * 2)

    @property
    def stack(self):
        return stack_thickness(self.card_count)

    @property
    def lid_length(self):
        return self.face - self.wall

    @property
    def face(self):
        return self.card.width + (self.wall * 2)

    # This is where I'll want to add height for the lid
    @property
    def height(self):
        return self.card.height + self.wall


class LocationBox(Partomatic):
    config: LocationBoxConfig = LocationBoxConfig()

    fillet: float = 2.0
    lid_head: float = 5

    @property
    def lid_inset(self):
        return self.lid_head / 2

    def magnet(self, center_x):
        m = self.config.magnet
        pos = Pos(
            center_x,
            self.config.depth / 2,
            self.config.height - self.lid_inset
        )
        return pos * Box(m.thickness + FIT, m.diameter + FIT, m.diameter + FIT)

    def compile(self):
        self.parts.clear()

        centered = (Align.MAX, Align.CENTER)

        # magnets
        mag = self.config.magnet
        box_magnet = self.magnet(self.config.wall - 0.25 - mag.thickness/2)
        lid_magnet = self.magnet(self.config.wall + 0.5 + mag.thickness/2)

        with BuildPart() as box:
            # Make the box & hollow it out
            Box(*self.coords, align=(Align.MIN, Align.MIN, Align.MIN))
            offset(amount=-self.config.wall, openings=faces().sort_by(Axis.Z)[-1])

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

            # magnet pocket in the back wall, just behind the closed seam
            add(box_magnet, mode=Mode.SUBTRACT)

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

        with BuildPart() as lid:
            extrude(offset(lid_key.sketch, -FIT), amount=-self.config.lid_length)
            extrude(faces().sort_by(Axis.Z)[-1], amount=FIT)
            extrude(head.sketch, amount=-self.config.wall)

            # matching magnet pocket in the lid tip, facing the box magnet
            add(lid_magnet, mode=Mode.SUBTRACT)

            ####################
            # Polish the edges
            verticals = edges().filter_by(Axis.Z).group_by(Axis.X)[-1]

            top   = edges().filter_by(Plane.XY).group_by(Axis.Z)[-1]
            sides = top.filter_by(Axis.X).group_by(Axis.Y)
            ends  = top.filter_by(Axis.Y).group_by(Axis.X)

            # we want the lid's edge to sit flush with the box itself
            lid_edges = verticals + sides[0] + sides[-1] + ends[-1]
            fillet(lid_edges, self.fillet)

        # Slide joint: the lid travels along the lid_plane normal, seated at 0
        LinearJoint(
            "slide", to_part=box.part,
            axis=Axis(lid_plane.origin, lid_plane.z_dir),
            linear_range=(0, self.config.lid_length),
        )
        RigidJoint("seat", to_part=lid.part, joint_location=Location(lid_plane.origin))
        box.part.joints["slide"].connect_to(lid.part.joints["seat"], position=0)

        # Set colors
        box.part.label = "box"
        box.part.color = Color(self.config.color)

        lid.part.label = "lid"
        lid.part.color = cshift(box.part.color)

        self.parts.append(
            AutomatablePart(
                box.part, f"{self.config.name} box.stl",
                display_location=Location((0, 0, 0)),
                stl_folder=self.config.stl_folder,
            )
        )

        self.parts.append(
            AutomatablePart(
                lid.part, f"{self.config.name} lid.stl",
                display_location=Location((0, 0, 0)),
                stl_folder=self.config.stl_folder,
            )
        )

    @property
    def coords(self):
        return [self.config.face, self.config.depth, self.config.height]

    @compiled
    def box(self):
        return self.parts[0].part

    @compiled
    def assembly(self):
        return Compound(
            label=self.config.name,
            children=[p.part for p in self.parts]
        )


if __name__ == "__main__":
    from ocp_vscode import show, Animation

    box = LocationBox()
    box.partomate()

    asm = box.assembly()
    show(asm, render_joints=True)

    slide = box.config.lid_length + 10
    anim = Animation()
    anim.add_track(f"/{box.config.name}/lid", "tx", times=[0, 1, 2], values=[0, slide, 0])
    anim.animate(speed=0.9)

    log.info("processed location_box")
