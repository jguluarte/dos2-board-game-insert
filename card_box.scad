module card_box(x, y, z, wall) {
    base = [x, y];

    card_shell(z, wall) square(base, true);
}

module card_shell(height, wall) {
    union() {
        linear_extrude(wall) offset(r=wall) children();
        linear_extrude(height + wall) difference() {
            offset(r=wall) children();
            children();
        }    
    }
}
