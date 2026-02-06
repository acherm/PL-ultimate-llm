/* Producer-Consumer example in C-Linda */
#include <linda.h>
#include <stdio.h>

/* Producer process */
void producer() {
    int i;
    for (i = 1; i <= 5; i++) {
        printf("Producer: sending %d\n", i);
        out("item", i);
    }
    out("done", 1);
}

/* Consumer process */
void consumer() {
    int value;
    int done = 0;

    while (!done) {
        if (inp("done", 1)) {
            done = 1;
        } else {
            in("item", ?value);
            printf("Consumer: received %d\n", value);
        }
    }
}

int main() {
    eval(producer());
    eval(consumer());
    return 0;
}
