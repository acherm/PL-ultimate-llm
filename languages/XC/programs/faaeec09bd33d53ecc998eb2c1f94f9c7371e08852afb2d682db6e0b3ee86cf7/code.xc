#include <platform.h>
#include <stdio.h>

void task1(chanend c) {
    c <: 1;
    printf("Task 1: sent value\n");
}

void task2(chanend c) {
    int value;
    c :> value;
    printf("Task 2: received %d\n", value);
}

int main(void) {
    chan c;
    par {
        task1(c);
        task2(c);
    }
    return 0;
}
