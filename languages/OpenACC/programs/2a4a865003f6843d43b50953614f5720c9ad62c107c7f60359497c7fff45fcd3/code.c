#include <stdio.h>
#include <stdlib.h>

int main() {
    int n = 1000000;
    float *a, *b, *c;
    
    // Allocate memory
    a = (float*)malloc(n * sizeof(float));
    b = (float*)malloc(n * sizeof(float));
    c = (float*)malloc(n * sizeof(float));
    
    // Initialize arrays
    for (int i = 0; i < n; i++) {
        a[i] = i * 1.0f;
        b[i] = i * 2.0f;
    }
    
    // Parallel vector addition using OpenACC
    #pragma acc parallel loop copyin(a[0:n], b[0:n]) copyout(c[0:n])
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
    
    // Verify result
    printf("c[0] = %f, c[999999] = %f\n", c[0], c[999999]);
    
    free(a);
    free(b);
    free(c);
    
    return 0;
}
