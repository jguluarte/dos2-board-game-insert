# OpenSCAD CLI lives inside the manually-installed .app (not on $PATH).
OPENSCAD := /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD

# Which part to act on. Override on the command line:
#   make stl PART=items_tray
PART ?= location_box
SRC  := $(PART).scad
STL  := build/$(PART).stl

.PHONY: stl preview clean

# Headless full render to STL (the F6-equivalent — final geometry, ready to slice).
stl: $(STL)

# Rebuild the STL only when the .scad is newer. `| build` is an order-only
# prerequisite: make the dir if missing, but don't rebuild just because it changed.
$(STL): $(SRC) | build
	$(OPENSCAD) -o $@ $<

# Open the part in the OpenSCAD GUI for the edit/auto-reload loop.
preview:
	open -a OpenSCAD $(SRC)

build:
	mkdir -p build

clean:
	rm -rf build
