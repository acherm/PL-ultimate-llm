(* Symja example: basic symbolic math operations *)
f[x_] := x^2 + 2*x + 1

(* Expand and factor *)
Expand[(x+1)^3]
Factor[x^2 + 2*x + 1]

(* Integration and differentiation *)
Integrate[x^2, x]
D[Sin[x]*Cos[x], x]

(* Solve equation *)
Solve[x^2 - 5*x + 6 == 0, x]
