/* Transportation Problem in GNU MathProg (GMPL) */

set ORIG;  /* origins */
set DEST;  /* destinations */

param supply{ORIG} >= 0;   /* supply at each origin */
param demand{DEST} >= 0;   /* demand at each destination */
param cost{ORIG, DEST} >= 0;  /* cost per unit shipped */

var x{ORIG, DEST} >= 0;   /* units shipped */

minimize total_cost:
    sum{i in ORIG, j in DEST} cost[i,j] * x[i,j];

s.t. supply_limit{i in ORIG}:
    sum{j in DEST} x[i,j] = supply[i];

s.t. demand_req{j in DEST}:
    sum{i in ORIG} x[i,j] = demand[j];

data;

set ORIG := Plant1 Plant2 Plant3;
set DEST := Whouse1 Whouse2 Whouse3;

param supply :=
    Plant1  120
    Plant2   80
    Plant3   80;

param demand :=
    Whouse1  150
    Whouse2   70
    Whouse3   60;

param cost :
              Whouse1  Whouse2  Whouse3 :=
    Plant1        2        3        1
    Plant2        5        4        8
    Plant3        5        6        8;

end;
