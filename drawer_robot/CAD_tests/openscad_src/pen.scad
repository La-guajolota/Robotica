// Plantilla paramétrica de un lápiz
module pencil(length = 150, radius = 5, tip_length = 20) {
    // Cuerpo del lápiz
    cylinder(h = length - tip_length, r = radius, center = false);

    // Punta del lápiz
    translate([0, 0, length - tip_length])
        cone(h = tip_length, r1 = radius, r2 = 0);
}

// Módulo para un cono
module cone(h, r1, r2) {
    cylinder(h = h, r1 = r1, r2 = r2, center = false);
}

// Llamada al módulo del lápiz
pencil();