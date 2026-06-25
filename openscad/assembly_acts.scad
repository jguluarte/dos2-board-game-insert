include <BOSL2/std.scad>

include <card_box.scad>
include <colors.scad>

use <gamebox.scad>

use <utils.scad>

/* Structs */
function _act(boxes, color) = struct_set([], [
    "color", color,
    "boxes", boxes,
    "sum",   sum([for (cards = boxes) locationFootprint(cards)]),
]);

locationFootprint = function(cards) addGap( wallify(STACKED(cards)) );

// Common accessors
__sum = function(a) struct_val(a, "sum");

function __boxes(a) = struct_val(a, "boxes");
module   __color(a) color(struct_val(a, "color")) children();

// Named versions of these acts
ACT_TUTORIAL     = _act([14], COLOR_TUTORIAL);
ACT_NEMESIS      = _act([32], COLOR_NEMESIS);
ACT_HAUNTED_KEEP = _act([45], COLOR_HAUNTED_KEEP);

ACT_1 = _act([56, 67, 61], COLOR_ACT1);
ACT_2 = _act([63, 51, 51], COLOR_ACT2);
ACT_3 = _act([41, 46, 36], COLOR_ACT3);

// This array is going to correspond to the "act identifier"
DEFAULT_ACTS = [
    ACT_TUTORIAL,
    ACT_1,
    ACT_2,
    ACT_3,
    ACT_HAUNTED_KEEP,
    ACT_NEMESIS,
];

module location_box(cards) {
    card_box(cards, TAROT, TALL, STACKED) children();
}

module act_boxes(act) {
    flow(__boxes(act), locationFootprint)
        __color(act) location_box($flow) children();
}

/******************************
 * START ASSEMBLY
 ******************************/

gamebox() locations_longwise();

// this builds on `__card_box_vars` <-- rename to `dynamic vars`
function __locations_longwise_vars() = __card_box_vars([
    ["$gap", $gap],
]);

// arrangement: acts run along the front wall, final act tucked
// back-right; call as a child of gamebox()
module locations_longwise() {
    $card_anchor = LEFT + BACK + BOT;

    __assert_dynamic_vars( __locations_longwise_vars() );

    // We have to position the "final act" differently...
    // it doesn't fit in the row :(
    final_act        = last(DEFAULT_ACTS);
    all_but_last_act = list_head(DEFAULT_ACTS);

    // the acts run along the front wall
    position(LEFT+FRONT+BOT) translate([$gap, $gap, $buffer])
        flow(all_but_last_act, __sum, $spin=90) act_boxes($flow);

    // tuck the final act into the back-right corner
    position(RIGHT+BACK+BOT) translate([-$gap, -$gap, $buffer])
        act_boxes(final_act, $spin=90, $card_anchor=RIGHT+FRONT+BOT);

    children();
}
