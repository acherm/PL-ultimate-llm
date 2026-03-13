;; JACAL polynomial operations example
;; Source: JACAL manual

e1 : x^2 - y^2;
e2 : factor(e1);

e3 : (x + y)^3;
e4 : expand(e3);

e5 : diff(x^3 + 2*x^2 + x, x);
