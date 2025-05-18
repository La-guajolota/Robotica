// Importing two modules
use <link.scad>;
use <pen.scad>;

// Parameters for the drawer
links_length = 100;       // Length of the link
links_width = 20;        // Width of the link
links_thickness = 10;    // Thickness of the link
hole_diameter = 15;     // Diameter of the holes
edge_tolerance = 1.5; // Tolerance for the hole fit
// Parameters for the pencil
pencil_length = 150;     // Length of the pencil
pencil_radius = hole_diameter/2;      // Radius of the pencil
pencil_tip_length = 20; // Length of the pencil tip

// Module for the drawer assembly
dist_between_links = 60; // Distance between the links
dist_between_link_origin = dist_between_links/2; // Distance between the origins of the links

// drawer assembly
// Position and assemble the modules
translate([0, -50, 0]){
    rotate([0, 0, 36]) {
        translate([50, 0, 0]) {
            link(links_length, links_width, links_thickness, hole_diameter);
        }
        translate([91, 0, 100]) {
            rotate ([0, 180, 0]){
                pencil(pencil_length, pencil_radius, pencil_tip_length);
            }
        }
    }
}
