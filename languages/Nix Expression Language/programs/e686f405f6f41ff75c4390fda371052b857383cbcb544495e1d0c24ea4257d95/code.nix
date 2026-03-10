let
  fibonacci = n:
    if n == 0 then 0
    else if n == 1 then 1
    else fibonacci (n - 1) + fibonacci (n - 2);
in
  builtins.map fibonacci (builtins.genList (x: x) 10)