/* Mentat example: Parallel sum computation
   The Mentat Programming Language by Andrew Grimshaw, UVA */

#include <mentat/mentat.h>
#include <stdio.h>

mentat class Summer : public MObject {
public:
    int sum(int start, int end);
};

int Summer::sum(int start, int end) {
    int total = 0;
    for (int i = start; i <= end; i++) {
        total += i;
    }
    return total;
}

int main(int argc, char *argv[]) {
    Summer s1, s2;

    /* Parallel method invocations - return immediately */
    int* h1 = s1.sum(1, 50);
    int* h2 = s2.sum(51, 100);

    /* Dereference blocks until results are available */
    printf("Sum of 1..100 = %d\n", *h1 + *h2);

    return 0;
}
