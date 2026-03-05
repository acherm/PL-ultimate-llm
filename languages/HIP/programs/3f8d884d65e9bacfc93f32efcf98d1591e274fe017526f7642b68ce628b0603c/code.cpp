#include <hip/hip_runtime.h>
#include <stdio.h>

#define THREADS_PER_BLOCK 256
#define N 1048576

__global__ void vectorAdd(const float *a, const float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    float *h_a, *h_b, *h_c;
    float *d_a, *d_b, *d_c;
    size_t size = N * sizeof(float);

    h_a = (float *)malloc(size);
    h_b = (float *)malloc(size);
    h_c = (float *)malloc(size);

    for (int i = 0; i < N; i++) {
        h_a[i] = (float)i;
        h_b[i] = (float)(N - i);
    }

    hipMalloc((void **)&d_a, size);
    hipMalloc((void **)&d_b, size);
    hipMalloc((void **)&d_c, size);

    hipMemcpy(d_a, h_a, size, hipMemcpyHostToDevice);
    hipMemcpy(d_b, h_b, size, hipMemcpyHostToDevice);

    int blocks = (N + THREADS_PER_BLOCK - 1) / THREADS_PER_BLOCK;
    hipLaunchKernelGGL(vectorAdd, dim3(blocks), dim3(THREADS_PER_BLOCK), 0, 0,
                       d_a, d_b, d_c, N);

    hipMemcpy(h_c, d_c, size, hipMemcpyDeviceToHost);

    printf("h_c[0] = %f\n", h_c[0]);
    printf("h_c[%d] = %f\n", N - 1, h_c[N - 1]);

    hipFree(d_a);
    hipFree(d_b);
    hipFree(d_c);
    free(h_a);
    free(h_b);
    free(h_c);

    return 0;
}
