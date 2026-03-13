/* CC++ (Compositional C++) parallel Fibonacci
 * Demonstrates par{} blocks for parallel task creation and sync variables.
 * K.M. Chandy & C. Kesselman, "CC++: A Declarative Concurrent
 * Object-Oriented Programming Notation", Caltech TR-92-02, 1992.
 */
#include <iostream>
using namespace std;

int fib(int n) {
    if (n <= 1) return n;
    sync int f1, f2;
    par {
        f1 = fib(n - 1);
        f2 = fib(n - 2);
    }
    return f1 + f2;
}

int main() {
    for (int i = 0; i <= 10; i++)
        cout << "fib(" << i << ") = " << fib(i) << endl;
    return 0;
}
