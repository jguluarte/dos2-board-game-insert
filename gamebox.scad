include <BOSL2/std.scad>

function interior() = [395, 303, 175];

/******************************
 * The measured box interior as an attachable BOSL2 parent.
 *
 * Children place themselves with the standard attachment modules:
 *
 *   gamebox() {
 *       position(BOT+BACK+LEFT) sectioned_box(items);
 *       position(BOT+BACK+RIGHT) act_boxes(...);
 *   }
 *
 * The interior volume ghosts itself (%) so it shows in preview but
 * never lands in a render/export — callers no longer need `%gamebox()`.
 *
 * Default anchor keeps the origin at the front-left-bottom corner,
 * matching the old `cube(INTERIOR)` world coordinates.
 ******************************/

module gamebox(anchor=FRONT+LEFT+BOT, spin=0, orient=UP) {
    attachable(anchor, spin, orient, size=interior()) {
        %cuboid(interior());
        children();
    }
}

gamebox();
