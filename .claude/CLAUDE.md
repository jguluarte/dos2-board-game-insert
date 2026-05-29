# D:OS Board Game Insert

Parametric 3D-printed insert for Divinity: Original Sin (base + 3 expansions + KS content).

## How to work with Justin on this project

**Coach, don't drive.** Justin is the modeler — he is intentionally learning OpenSCAD through this project. Provide reference material, math, parametric structure suggestions, tolerance reasoning, and review of his code. Do **not** produce finished SCAD on his behalf unless he explicitly asks. When he is stuck, ask what he has tried before showing a solution.

**Editor separation.** Justin uses Sublime Text + OpenSCAD GUI (file-watch reload). Stay in the terminal. Do not offer to edit files in Sublime on his behalf or push him toward VSCode/IDE-integrated tooling.

**Anti-drift anchor.** Flag substitution pivots (changing topic because of friction) vs information-driven pivots (changing topic because new info made it the right call). The latter is fine. The former needs surfacing.

## Locked decisions

### Tool choice
- **OpenSCAD (snapshot build)** for parts — installed manually (Justin avoids Homebrew). The stable release is Intel-only; the snapshot runs native arm64.
- **FreeCAD optional, for pretty assembly visualization only** if Justin wants it at the end. Functional collision-check and layout happens in OpenSCAD itself.

### OpenSCAD assembly pattern
Top-level `assembly.scad` imports all part modules and `translate()`s them into position inside a transparent `%cube(box_interior)` ghost. Collision check via `intersection() { part_a(); part_b(); }` — empty render = no overlap.

```scad
// assembly.scad sketch
use <location_box.scad>;
use <items_tray.scad>;

box_interior = [TBD, TBD, TBD];  // not yet measured

%cube(box_interior);  // transparent reference

translate([0, 0, 0]) location_box();
translate([130, 0, 0]) items_tray();
```

### Tolerances (Ryker sleeves, 110-120 µm)
- **X:** +0.8 mm/side (1.6 mm total) — validated on location stack measurement
- **Y:** +0.7 mm/side (1.4 mm total) — validated on location stack measurement
- **Z (stack height):** +10-15% headroom over measured stack height. Sleeved stacks compress when measured (air bleeds from sleeves under finger pressure); modeled depth needs the headroom or cards bind on extraction.
- **Reference fit data:** community-designed sleeved well (45×68×10mm) confirmed Ryker fit in this box's printed environment.

### Card sizes (unsleeved → modeled-with-tolerance)
| Type | Unsleeved | Modeled well (with above tolerance) |
| -- | -- | -- |
| Standard American | 56 × 87 mm | derive from per-deck measurement |
| Mini American | 41 × 63 mm | derive from per-deck measurement |
| Tarot | 70 × 120 mm | derive from per-deck measurement |
| Location stack (measured) | 123.4 × 73.6 mm | **125 × 75 mm** |

Always measure the actual sleeved stack, don't trust card-size specs alone — sleeve thickness varies.

### Scope
- **Mini upgrade boxes stay external** to the main game box. Not modeling wells for minis.
- **Mini cards modeled last.** A status organizer already handles them during play; minis live near top of insert for quick session access.
- **Sequencing priority:**
  1. Location decks (the missing geometry in the existing stasyok base — solve it first)
  2. Expansion content
  3. Mini cards
- **Lid lift acceptable** — don't constrain volume to a perfectly flush close.

## Current state

- Tool choice and tolerances locked (above)
- Existing base insert in box = stasyok community print; has gaps: no location wells, center-bag overflow, unused box volume around insert footprint
- First piece to model: **location box** at 125×75 well dimensions, depth pending decision on access pattern (deferred — getting hands dirty on code-driven modeling first)
- Box interior L×W×H still uncaptured — needed before assembly layout but NOT needed for first standalone well print
- Per-deck card counts still uncaptured — needed when sizing other wells, not the location box

## Iteration loop

1. Model one well in isolation as a thin-walled test (2 mm walls, 2 mm floor, no lid)
2. Print at 15-20 min budget
3. Validate: sleeve fit (slides in without binding), extraction (finger pinch lifts cards without surgery)
4. Tune tolerance constants in SCAD if needed
5. Reprint test
6. Once a card-size well works, scale to real geometry by changing module inputs

Do not model the full insert before validating a single well.

## Reference

- [stasyok base insert](https://www.printables.com/model/1001670-divinity-original-sin-all-in-bottom-insert-replace) — what's already in the box
- [Sigismond0 Slay the Spire insert](https://www.printables.com/model/200862) — inspiration pattern (sharp internal pockets, function-grouped pull-out trays)
- [mychaos status organizer](https://www.printables.com/model/754771-divinity-original-sin-board-game-status-organizer) — handles minis during play

## BOSL2 (when ready)

[BOSL2](https://github.com/BelfrySCAD/BOSL2) adds proper attachment, anchoring, and rounded primitives to OpenSCAD. Worth introducing once Justin is comfortable with base OpenSCAD syntax — not on day one. Closes most of OpenSCAD's organic-shape gap and will simplify the parametric well module substantially.
