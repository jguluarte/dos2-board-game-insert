# D:OS Board Game Insert

Parametric 3D-printed insert for Divinity: Original Sin (base + 3
expansions + KS content). Built in OpenSCAD + BOSL2.

- `assembly.scad` — the full insert layout in the measured box interior
- `card_box.scad` / `location_box.scad` — parts
- `constants.scad` — shared `$` knobs + BOSL2 include; every file
  includes it (use `include`, not `use` — `use` strips variables)
- `docs/` — location deck data and box cut sheets
