#include <split-c.h>

global int *array::[PROCS];
int mysum, totalsum;

void main(void) {
  int i;

  /* Initialize distributed array */
  array = all_malloc(100 * sizeof(int));

  /* Each processor computes local sum */
  mysum = 0;
  for (i = 0; i < 100; i++) {
    array[i] = i;
    mysum += array[i];
  }

  /* Global reduction to compute total */
  totalsum = reduce_add(mysum);

  if (MYPROC == 0)
    printf("Total sum: %d\n", totalsum);
}
