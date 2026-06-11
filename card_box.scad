include <BOSL2/std.scad>
include <constants.scad>

use <utils.scad>

/******************************
 * Kinds of cards
 ******************************/

// define a kind of card
function __card(long, short) = struct_set([], [
    "long",  long,
    "short", short,
]);

STANDARD = __card(
    long  = $sleeve__standard__long,
    short = $sleeve__standard__short,
);

TAROT = __card(
    long  = $sleeve__tarot__long,
    short = $sleeve__tarot__short,
);

function long_side(c)  = struct_val(c, "long");
function short_side(c) = struct_val(c, "short");

/******************************
 * Strategies
 ******************************/

// Card orientation strategies

// x=t.short -- y=cards -- z=t.long
TALL = function (c, cards, height_multiplier=1) [
    short_side(c),
    cards,
    long_side(c) * height_multiplier,
];

// x=t.long -- y=cards -- z=t.short
WIDE = function (c, cards, height_multiplier=1) [
    long_side(c),
    cards,
    short_side(c) * height_multiplier,
];

// x=t.long -- y=t.short -- z=cards
TRAY = function (c, cards, height_multiplier=1) [
    long_side(c),
    short_side(c),
    cards * height_multiplier,
];

// Packing strategies

// strategy used to create a single card well
STACKED = function (cards) (cards * $sleeved_thickness) + $card_clearance;

// used to calculate opening required for many holes
SECTIONED = function (s) sum(_openings(s)) + (len(s) - 1) * $section_divider;

// we have lots of little openings when SECTIONED, so leverage STACKED
function _openings(card_array) = [for (cards = card_array) STACKED(cards)];

/******************************
 * Card Geometry
 ******************************/

module card_box(cards, type, orientation, strategy) {
    __assert_dynamic_vars( __card_box_vars() );

    // Set object context for "child" operations to this box
    $cards = cards;
    $card_type = type;
    $card_orientation = orientation;

    // `strategy` will return the space required for this kind of box
    card_space = strategy(cards);

    // `orientation` is a function which converts a card type
    // into the negative inner space required for this box
    hole =  orientation(type, card_space);

    // Add the side walls and floor such that `box` is the outer shell
    box = hole + [wallify(), wallify(), $wall];

    diff()
    cuboid(box, anchor=$card_anchor, spin=$spin, orient=$orient) {

        // drill out the `hole` for the box
        position(TOP) up($buffer)
            tag("remove") cuboid(hole, anchor=TOP);

        children();
    };
}

function __card_box_vars(extra=[]) = [
    ["$spin", $spin],
    ["$wall", $wall],
    ["$buffer", $buffer],
    ["$orient", $orient],
    ["$card_anchor", $card_anchor],
    ["$card_clearance", $card_clearance],
    ["$section_divider", $section_divider],
    ["$sleeved_thickness", $sleeved_thickness],
    each extra,
];

module sections() {
    __assert_dynamic_vars( __sections_vars() );

    corner = FRONT + BOTTOM;

    mult = $section_height_multiplier;

    // we can reuse the strategy here to calculate the size of the divider :)
    divider = $card_orientation($card_type, $section_divider, mult) + [$wall, 0, 0];

    for (pos = section_wall_positions($cards)){
        position(corner)
            back($wall - $section_divider + pos)
            tag("keep") cuboid(divider, anchor=corner);
    };
}

function __sections_vars() = __card_box_vars([
    ["$cards", $cards],
    ["$card_type", $card_type],
    ["$card_orientation", $card_orientation],
    ["$section_height_multiplier", $section_height_multiplier],
]);

// calculate each wall's starting position potion.
// Include $section_divider so each subsequent wall will factor in previous walls
function section_wall_positions(cards) = list_head(
    cumsum([for (c = cards) STACKED(c) + $section_divider])
);
