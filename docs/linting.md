# In-editor linting for OpenSCAD (Sublime)

Goal: see OpenSCAD's warnings (redefined variables, unknown variables, parse
errors) as a gutter mark in Sublime — where your eyes already are — instead of
only in the OpenSCAD console.

## Why it's built this way

OpenSCAD's language servers (openscad-lsp and friends) are **tree-sitter based**:
they parse the grammar but don't *evaluate* the script. The warning that matters
most — `"x" was assigned ... but was overwritten` — comes from the evaluator's
last-wins scope resolution, not the parser. No LSP reports it.

The only thing that knows is the **openscad binary itself**. So the linter shells
out to it and parses its output, using CSG export (`-o - --export-format csg`),
which *evaluates* the script (triggering the warnings) but skips the heavy
geometry render — about 25ms on a small file.

## The pieces (all in Sublime config, not this repo)

| File | Role |
| -- | -- |
| `Packages/User/openscad_linter.py` | Custom SublimeLinter plugin: lint command + regex. Bound to `source.scad`. |
| `Packages/User/SublimeLinter.sublime-settings` | `lint_mode`, gutter styles. |
| `Packages/SublimeLinter/` | The SublimeLinter framework — **installed from source** (git clone), not Package Control, which refused to serve it. |
| `Lib/python3.8/typing_extensions.py` | SublimeLinter's one dependency, placed by hand (PC would normally do this). Pinned to 4.12.2 — the last release supporting the 3.8 plugin host. |

The OpenSCAD binary path is hardcoded in `openscad_linter.py` (`OPENSCAD = ...`)
because OpenSCAD isn't on `$PATH` and GUI Sublime doesn't inherit the shell `$PATH`.

## Two gotchas baked into the plugin (don't undo these)

1. **`on_stderr = None`.** OpenSCAD writes warnings to stderr. By default
   SublimeLinter parses *stdout* and treats stderr as a linter *failure*. Setting
   `on_stderr = None` flips it to parse the combined output, so the warnings
   actually reach the regex.
2. **Spaces in the regex.** Harmless here (SublimeLinter compiles with no flags),
   but if you ever see a match fail, check whether VERBOSE got turned on — then
   literal spaces would be ignored and you'd need `\s`.

## Using it

- **On save:** automatic (`lint_mode: save`).
- **On demand:** Command Palette → `SublimeLinter: Lint this view`.
- **See the message:** hover the gutter mark or the highlighted code, or put the
  cursor on the line (status bar). `SublimeLinter: Show all errors` lists them.

## Maintenance note

SublimeLinter is a source clone, so Package Control won't auto-update it. To
update: `git pull` in `Packages/SublimeLinter/`. If a future version needs a
newer dependency, drop it into `Lib/python3.8/`.

## Verifying / debugging

Run the exact lint command by hand to see what Sublime sees:

```
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD \
    -o - --export-format csg path/to/file.scad
```

Any `WARNING:`/`ERROR:` line with `... line N` becomes a mark on line N. For
deeper issues: Command Palette → `SublimeLinter: Enable Debug Logging`.
