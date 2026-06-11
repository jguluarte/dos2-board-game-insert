include <BOSL2/std.scad>

/******************************
 * Lid
 *
 * A flat cap with a registration lip that rides as a CHILD of card_box.
 * It discovers the box's outer size from the attach context ($parent_size),
 * so it stays decoupled from how card_box sized itself. The only ambient
 * knob it needs is $wall, which is already in scope wherever card_box runs.
 *
 *   card_box(cards, STANDARD, TALL, STACKED) lid();
 *   card_box(...) lid(fit=0.3);   // looser print fit
 *   card_box(...) lid(lift=20);   // exploded preview, raised off the box
 *   card_box(...) %lid();         // ghost it in the closed position
 *
 *   fit   per-side clearance between the lip and the box interior
 *   depth how far the registration lip reaches into the opening
 *   lift  raise the lid this far above the box (0 = closed / in place)
 ******************************/

module lid(fit=0.2, depth=6, lift=0) {
    assert(!is_undef($parent_size),
        "lid() must be a child of a sized parent (e.g. card_box)");

    box = $parent_size;                       // outer [x, y, z]
    cap = [box.x, box.y, $wall];
    lip = [box.x - 2*($wall + fit),
           box.y - 2*($wall + fit),
           depth];

    // tag("keep") so card_box's hole removal doesn't eat the lip
    position(TOP) up(lift)
        tag("keep")
        union() {
            cuboid(cap, anchor=BOTTOM);       // cap rests on the rim
            cuboid(lip, anchor=TOP);          // lip drops into the opening
        }
}

/******************************
 * Snap lid — lid() plus a side skirt with horizontal print-in-place magnets.
 *
 * A downward skirt hugs the box's right exterior wall. A box-side magnet
 * pocket is cut into that wall (it rides in card_box's diff as a remove);
 * a lid-side pocket sits in the skirt. Both magnets are X-axis discs at the
 * SAME height, so they meet across the seam and snap the lid closed.
 *
 * Magnets are pause-at-layer drops: print to the magnet's layer, set the
 * disc in, resume — the `skin` wall seals it, no support, no nozzle jump.
 *
 *   card_box(...) snap_lid();
 *   card_box(...) snap_lid(lift=18);   // exploded preview
 *
 *   mag_d / mag_h  magnet disc diameter / thickness (e.g. 6 x 2)
 *   skin           plastic between a magnet face and the surface
 ******************************/

module snap_lid(fit=0.2, depth=6, lift=0, mag_d=6, mag_h=2, skin=0.8) {
    assert(!is_undef($parent_size),
        "snap_lid() must be a child of a sized parent (e.g. card_box)");

    box     = $parent_size;
    mag_off = mag_d / 2 + 1;              // magnet center, below the rim
    skirt   = [mag_h + 2*skin, box.y, mag_d + 4];

    // ---- box-side pocket: cut into the box's right wall ----
    position(RIGHT) up(box.z/2 - mag_off) left(skin)
        tag("remove") xcyl(d=mag_d, l=mag_h + $buffer, anchor=RIGHT);

    // ---- the lid (lifts as a unit; its own diff keeps the skirt pocket local) ----
    position(TOP) up(lift)
        tag("keep")
        diff() {
            union() {
                cuboid([box.x, box.y, $wall], anchor=BOTTOM);                          // cap
                cuboid([box.x - 2*($wall + fit),
                        box.y - 2*($wall + fit), depth], anchor=TOP);                  // lip
                right(box.x/2) cuboid(skirt, anchor=LEFT+TOP);                          // skirt hugs the wall
            }
            // lid-side pocket in the skirt, aligned to the box pocket
            right(box.x/2 + skin) down(mag_off)
                tag("remove") xcyl(d=mag_d, l=mag_h + $buffer, anchor=LEFT);
        }
}
