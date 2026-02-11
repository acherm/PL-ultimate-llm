/*@ requires \valid(a) && \valid(b);
  @ ensures \result == *a || \result == *b;
  @ ensures \result >= *a && \result >= *b;
  @*/
int max(int *a, int *b) {
  if (*a > *b)
    return *a;
  else
    return *b;
}

/*@ requires n >= 0;
  @ requires \valid(arr + (0..n-1));
  @ ensures \result >= 0 && \result < n;
  @ ensures \forall integer k; 0 <= k < n ==> arr[\result] >= arr[k];
  @*/
int max_array(int *arr, int n) {
  int max_idx = 0;
  /*@ loop invariant 0 <= i <= n;
    @ loop invariant 0 <= max_idx < n;
    @ loop invariant \forall integer k; 0 <= k < i ==> arr[max_idx] >= arr[k];
    @ loop variant n - i;
    @*/
  for (int i = 1; i < n; i++) {
    if (arr[i] > arr[max_idx])
      max_idx = i;
  }
  return max_idx;
}