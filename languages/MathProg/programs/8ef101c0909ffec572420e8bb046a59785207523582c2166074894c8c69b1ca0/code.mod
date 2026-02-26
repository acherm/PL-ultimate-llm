/* Simple LP in MathProg (GMPL): Production planning */
/* Maximize profit subject to resource constraints */

var x1 >= 0;   /* units of product 1 */
var x2 >= 0;   /* units of product 2 */
var x3 >= 0;   /* units of product 3 */

maximize profit: 10*x1 + 6*x2 + 4*x3;

s.t. labor:    x1 + x2 + x3 <= 100;
s.t. machine:  10*x1 + 4*x2 + 5*x3 <= 600;
s.t. material: 2*x1 + 2*x2 + 6*x3 <= 300;

solve;

printf "Optimal production quantities:\n";
printf "  x1 = %g\n", x1;
printf "  x2 = %g\n", x2;
printf "  x3 = %g\n", x3;
printf "Maximum profit: %g\n", profit;

end;
