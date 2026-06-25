include <BOSL2/std.scad>
include <constants.scad>

use <utils.scad>

/**************************************
 * Deck data
 *
 * Expects BOSL2 + card_box.scad + colors.scad from the includer.
 * Decks are authored as [count, label] rows — the labels are
 * comments that stay attached to the data. Only the counts make
 * it into the struct.
 **************************************/

function _deck(color, rows) = let (counts = column(rows, 0)) struct_set([], [
    "color",    color,
    "sections", counts,
    "depth",    wallify( SECTIONED(counts) ),
]);

function __depth(d)    = struct_val(d, "depth");
function __sections(d) = struct_val(d, "sections");

JOURNALS = _deck("pink", [
    [68, "base"],
    [03, "haunted keep"],
    [13, "nemesis"],
]);

ITEMS = _deck("maroon", [
    [46, "item: 1"],
    [18, "item: 2"],
    [18, "item: 3"],
    [25, "item: 4"],
    [21, "item: 5"],
    [23, "item: 6"],
    [23, "item: unique"],
    [08, "consumable: arrows"],
    [15, "consumable: grenades"],
    [24, "consumable: potions"],
    [15, "consumable: scrolls"],
]);

MINIONS = _deck("skyblue", [
    [123, "minions"],
]);

SKILLS = _deck("purple", [
    [11, "aerotheurge"],
    [11, "geomancer"],
    [11, "hydrosophist"],
    [11, "pyrokinetic"],
    [11, "necromancer"],
    [11, "polymorph"],
    [11, "summoning"],
    [11, "warfare"],
    [11, "two-handed"],
    [11, "scoundrel"],
    [11, "duelist"],
    [11, "huntsman"],

    [18, "demonology"],
    [16, "summons"],
]);

TUTORIAL = _deck(COLOR_TUTORIAL, [
    [40, "tutorial"],
]);

CHARACTERS = _deck("seagreen", [
    [6, "vali"],
    [6, "fane"],
    [6, "ifan"],
    [6, "lohse"],
    [6, "beast"],
    [6, "cassian"],
    [6, "tanguistal"],
    [6, "farzanah"],
    [6, "the red prince"],
    [6, "sebille"],

    [12, "collars + vampirism + hex"],
]);

// recovered from count; sums to manifest 91 (L4 ~approx)
DUNGEONS = _deck("grey", [
    [20, "level 1"],
    [16, "level 2"],
    [11, "level 3"],
    [21, "level 4"],
    [16, "level 5"],
    [07, "bosses"],
]);

BOSSES = _deck("red", [
    [26, "act 1"],
    [35, "act 2"],
    [78, "act 3"],
    [08, "haunted keep"],
    [11, "nemesis"],
]);
