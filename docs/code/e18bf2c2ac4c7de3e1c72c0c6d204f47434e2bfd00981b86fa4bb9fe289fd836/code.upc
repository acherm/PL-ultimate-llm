#include <upc.h>
#include <stdio.h>

shared int foo;

int main() {
  if (MYTHREAD==0) foo = 42;
  upc_barrier;
  printf("THREAD %d sees foo = %d\n", MYTHREAD, foo);
  return 0;
}