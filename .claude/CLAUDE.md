# D:OS Board Game Insert

## Before touching code or design — read the memory files
Read the memory FILES in `~/.claude/projects/-Users-jguluarte-cad-dos2-board-game/memory/`
(`dos2-build123d`, `dos2-project-state`, `dos2-design-rules`,
`dos2-print-log`), not just the auto-loaded `MEMORY.md` index. He lives in
the ocp-vscode viewer — run models with `watch.py`; a headless compile is
NOT proof a part looks right. Do only what was asked.

Parametric 3D-printed insert for Divinity: Original Sin (base + 3
expansions + KS content). Built in build123d (Python, on OCP/OpenCASCADE)
with partomatic; viewed in ocp-vscode. (Ported from OpenSCAD — that port is
complete and the `openscad/` tree has been removed.)

- `src/gamebox.py` — the full insert layout: places every box in the
  measured box interior (395×303×175)
- `src/location_box.py` — the location card box (sliding key-lid + magnets)
- `src/item_box.py` — `SectionedBox`: standard card box with non-uniform
  sections and a filleted finger notch
- `src/parts.py` — shared base (`Partomatic`, `Card`, `CardBoxConfig`)
- `src/acts.yaml` / `src/boxes.yaml` — deck data (card counts per box)
- `src/utils.py` — `WALL`, `stack_thickness`, `prime`, `compiled`
- `watch.py` — warm-reload loop; launches the ocp-vscode viewer (port 3939)
- `docs/` — location deck data and box cut sheets
