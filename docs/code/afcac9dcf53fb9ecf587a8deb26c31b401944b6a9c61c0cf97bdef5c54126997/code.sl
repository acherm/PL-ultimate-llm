fibonacci(n) :=
    let
        fibs[i] := 1 when i <= 2
                else fibs[i-1] + fibs[i-2];
    in
        fibs[n];

main := fibonacci(1 ... 10);
