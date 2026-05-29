// location_box.scad
// ----------------------------------------------------------------------------
// A single open-topped card well: the minimal thin-wall test print from the
// iteration loop. Outer block, carved out to leave 2mm walls + a 2mm floor.
//
// This is the smallest useful OpenSCAD shape: a box minus a smaller box.
// Everything else in the insert is a variation on it.
// ----------------------------------------------------------------------------


// ---- Module: location_box --------------------------------------------------
// A `module` is the closest thing OpenSCAD has to a class/function. The named
// arguments with defaults act like constructor defaults — call it bare to get
// the defaults, or override any of them: location_box(depth = 45);
//
// Units are millimeters throughout (OpenSCAD is unitless; the slicer reads mm)

module location_box(
        x       = 125,   // card footprint, long edge (location stack + tolerance)
        y       = 75,    // card footprint, short edge
        depth   = 30,    // cavity depth — PLACEHOLDER, real depth pending stack measurement
        wall    = 2,     // side-wall thickness
        floor_t = 2)     // floor thickness
{
    // A vector [x, y, z]. The outer block adds a wall on each of the 4 sides
    // and one floor underneath. This is a local variable — scoped to the module.
    outer = [x + 2 * wall, y + 2 * wall, depth + floor_t];


    // difference() = take the FIRST child, then subtract every child after it.
    // Solid block  minus  inner cavity  = an open-topped tray.
    difference() {

        // (1) the solid outer block, corner sitting at the origin
        cube(outer);

        // (2) the cavity to remove. translate() shifts it up by the floor
        //     thickness and inward by one wall on x and y, so what's left is
        //     floor + four walls. The +0.2 overshoot on z pokes the cavity
        //     through the top face so the well is cleanly open — without it
        //     you'd get a paper-thin skin across the top (a "z-fighting" artifact).
        translate([wall, wall, floor_t])
            cube([x, y, depth + 0.2]);
    }
}


// ---- Render ----------------------------------------------------------------
// This bare call is what draws when you open THIS file. Later, assembly.scad
// will `use <location_box.scad>;` — `use` imports the module but ignores this
// bottom-level call, so importing won't dump a stray box into the assembly.
// (`include <>` would run it; `use <>` won't. That distinction matters.)

location_box();
