include <BOSL2/std.scad>

// pad by $buffer
function buffer(x) = x + $buffer;

function addGap(size) = size + $gap;

// add dual walls
function wallify(x=0) = x + (2 * $wall);

// place objs along `dir`, each offset by the summed measures of
// those before it. Sets $flow for each child.
module flow(objs, measure, dir=RIGHT) {
    footprints = [for (o = objs) measure(o)];

    // for the first iteration...don't move the cursor
    position = [0, each cumsum(footprints)];

    for (i = idx(objs)) {
        $flow = objs[i];

        translate(position[i] * dir) children();
    }
}

module __assert_dynamic_vars(vars) {
    for (p = vars) let (key = p[0], val = p[1])
        assert(!is_undef(val), str("ERROR: `", key, "` is undefined"));
}
