// Gmsh GEO tutorial 1: Geometry basics, elementary entities, physical groups
// From the official Gmsh tutorials
// https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/tutorials/t1.geo

lc = 1e-2;

Point(1) = {0, 0, 0, lc};
Point(2) = {.1, 0,  0, lc};
Point(3) = {.1, .1, 0, lc};
Point(4) = {0,  .1, 0, lc};

Line(1) = {1, 2};
Line(2) = {3, 2};
Line(3) = {3, 4};
Line(4) = {4, 1};

Curve Loop(1) = {4, 1, -2, 3};

Plane Surface(1) = {1};

Physical Curve("Boundary") = {1, 2, 3, 4};
Physical Surface("My surface") = {1};
