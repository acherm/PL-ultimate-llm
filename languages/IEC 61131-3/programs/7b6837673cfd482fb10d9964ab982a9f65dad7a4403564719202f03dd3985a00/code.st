PROGRAM FibonacciCalc
VAR
    n      : INT := 10;
    a, b   : INT;
    temp   : INT;
    i      : INT;
    result : INT;
END_VAR

(* Compute the nth Fibonacci number using iteration *)
a := 0;
b := 1;
FOR i := 1 TO n DO
    temp := a + b;
    a := b;
    b := temp;
END_FOR;
result := a;
END_PROGRAM
