// Plantilla paramétrica para diseñar un eslabón rectangular con huecos circulares en las puntas

// Parámetros
length = 100;       // Largo del eslabón
width = 20;         // Ancho del eslabón
thickness = 10;     // Grosor del eslabón
hole_diameter = 15; // Diámetro de los huecos circulares
edge_tolerance = 1.5; // Tolerancia para el ajuste de los agujeros

module link(length, width, thickness, hole_diameter) {
    // Cuerpo principal del eslabón
    difference() {
        cube([length, width, thickness], center = true);
        
        hole_dist = length / 2 - hole_diameter / 2 - edge_tolerance;

        // Hueco circular en el extremo izquierdo
        translate([-hole_dist, 0, 0])
            cylinder(r = hole_diameter / 2, h = thickness + 1, center = true);
        
        // Hueco circular en el extremo derecho
        translate([hole_dist, 0, 0])
            cylinder(r = hole_diameter / 2, h = thickness + 1, center = true);
    }
}

// Llamada al módulo para generar el eslabón
link(length, width, thickness, hole_diameter);