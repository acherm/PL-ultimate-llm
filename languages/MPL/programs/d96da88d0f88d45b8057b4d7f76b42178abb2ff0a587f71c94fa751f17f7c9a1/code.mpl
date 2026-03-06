TITLE Production Planning

INDEX
  products = (A, B, C);

DATA
  profit[products] := A 5, B 4, C 3;
  labor[products]  := A 6, B 4, C 2;
  machine[products]:= A 3, B 2, C 5;

  labor_cap   = 240;
  machine_cap = 270;

MAX
  TotalProfit = SUM(p IN products: profit[p] * x[p]);

SUBJECT TO
  LaborCap:   SUM(p IN products: labor[p]   * x[p]) <= labor_cap;
  MachineCap: SUM(p IN products: machine[p] * x[p]) <= machine_cap;

BOUNDS
  x[products] >= 0;

END
