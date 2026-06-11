include <BOSL2/std.scad>

include <card_box.scad>
include <colors.scad>

use <gamebox.scad>

use <utils.scad>

use <assembly_acts.scad>

/**************************************
 * Current ideated boxes & sections
 **************************************/

// moved to condense space in this file
include <std_box_vars.scad>

// for quick reference
standard_boxes =[
    // ITEMS,       // 236
    // SKILLS,      // 166
    // BOSSES,      // 158
    // MINIONS,     // 123
    // DUNGEONS,    // 91
    // JOURNALS,    // 84
    // CHARACTERS,  // 72
    // TUTORIAL,    // 40
];

/**************************************
 * ASSEMBLE!
 **************************************/

STD_WIDTH = wallify(short_side(STANDARD));

module sectioned_box(deck) {
    $card_anchor = LEFT + BACK + BOT;

    card_box(__sections(deck), STANDARD, TALL, SECTIONED){
        sections();
        children();
    };
}

// slot `num` along the back wall, counting from the left;
// decks flow forward from the wall, spaced by their footprints
module backRow(num, decks=[]) {
    x = $gap + (num * addGap(STD_WIDTH));

    footprint = function(d) addGap( __depth(d) );

    position(LEFT+BACK+BOT) translate([x, -$gap, $buffer])
        flow(decks, footprint, FWD)
            __color($flow) sectioned_box($flow);
}

gamebox() {
    // First pass placing standard boxes in
    locations_longwise();

    backRow(0, [ITEMS]);
    backRow(1, [SKILLS, TUTORIAL]);
    backRow(2, [MINIONS, DUNGEONS]);
    backRow(3, [BOSSES]);
    backRow(4, [CHARACTERS, JOURNALS]);
}


echo("interior().y - $gap - wallify(short_side(TAROT)) - __depth(ITEMS) - $gap - $gap == ");
echo(interior().y - $gap - wallify(short_side(TAROT)) - __depth(ITEMS) - $gap - $gap);
