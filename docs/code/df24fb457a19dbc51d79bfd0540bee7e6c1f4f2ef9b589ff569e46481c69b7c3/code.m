// Compute Fibonacci numbers using matrix exponentiation
// This demonstrates Magma's matrix operations

function FibonacciMatrix(n)
    if n eq 0 then
        return 0;
    elif n eq 1 then
        return 1;
    end if;

    M := MatrixRing(IntegerRing(), 2);
    F := M![1, 1, 1, 0];

    result := F^(n-1);
    return result[1,1];
end function;

// Compute first 15 Fibonacci numbers
printf "First 15 Fibonacci numbers:\n";
for i := 0 to 14 do
    printf "%o ", FibonacciMatrix(i);
end for;
printf "\n";