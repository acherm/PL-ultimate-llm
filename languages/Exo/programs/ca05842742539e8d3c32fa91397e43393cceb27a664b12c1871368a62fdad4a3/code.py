from exo import *
from exo.platforms.x86 import AVX2
from exo.stdlib.scheduling import *

@proc
def gemm(N: size, M: size, K: size,
         C: f32[N, M] @ DRAM,
         A: f32[N, K] @ DRAM,
         B: f32[K, M] @ DRAM):
    for i in seq(0, N):
        for j in seq(0, M):
            for k in seq(0, K):
                C[i, j] += A[i, k] * B[k, j]

# Schedule: tile and vectorize
gemm_tiled = (gemm
    .rename('gemm_tiled')
    .split('i', 4, ['io', 'ii'], tail='cut_and_guard')
    .split('j', 4, ['jo', 'ji'], tail='cut_and_guard')
    .reorder('ii', 'jo')
    .reorder('ii', 'k')
)

print(gemm_tiled)
