#include <oxstd.h>

fib(const n)
{
    decl a = 0, b = 1;
    for (decl i = 0; i < n; ++i)
    {
        print(a, " ");
        decl temp = a + b;
        a = b;
        b = temp;
    }
    println("");
}

main()
{
    println("Fibonacci sequence:");
    fib(20);

    // Matrix operations example
    decl mA = < 1, 2; 3, 4 >;
    decl mB = < 5, 6; 7, 8 >;
    decl mC = mA * mB;
    println("Matrix A:");
    print(mA);
    println("Matrix B:");
    print(mB);
    println("Matrix A * B:");
    print(mC);
}
