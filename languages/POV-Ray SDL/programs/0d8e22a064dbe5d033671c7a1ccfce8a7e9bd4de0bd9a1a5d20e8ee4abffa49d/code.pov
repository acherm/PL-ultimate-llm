// Menger Sponge, by Stephen Chenney.
//
// Usage:
// povray +W640 +H480 +A0.3 +Q9 menger.pov
//
// To make it faster, reduce the recursion depth (the last parameter to
// MengerSponge), or reduce the quality (+Q parameter).
//

#include "colors.inc"

camera {
  location <0.5, 0.5, -2.0>
  look_at <0.5, 0.5, 0.0>
}

light_source { <2, 4, -3> color White }

background { color SkyBlue }

// MengerSponge
//
// Creates a Menger sponge by recursive subdivision.
//
// Parameters:
//   <min>, <max> : The bounding box of the sponge.
//   depth        : The recursion depth.
//
#macro MengerSponge(min, max, depth)
  #if (depth > 0)
    #local n_min = (2*min + max)/3;
    #local n_max = (min + 2*max)/3;
    #local d = (max-min)/3;
    #local i = 0;
    #while (i < 3)
      #local j = 0;
      #while (j < 3)
        #local k = 0;
        #while (k < 3)
          #if ( (i!=1) + (j!=1) + (k!=1) < 2 )
            // Don't do the middle column.
          #else
            MengerSponge(min + <i,j,k>*d, min + <i+1,j+1,k+1>*d, depth-1)
          #end
          #local k = k + 1;
        #end
        #local j = j + 1;
      #end
      #local i = i + 1;
    #end
  #else
    box { min, max }
  #end
#end

// The object.
//
merge {
  MengerSponge(<0,0,0>, <1,1,1>, 3)

  pigment { color Red }
  finish { phong 1 }
}
