#include "colors.inc"

camera { location <0,0,-3> look_at <0,0,0> }
light_source { <10,10,-10> White }

sphere { <0,0,0>,1
    texture {
        pigment { color Blue }
        finish { phong 1 }
    }
}
