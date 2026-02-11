fn matmul(C: Matrix, A: Matrix, B: Matrix):
    for m in range(C.rows):
        for k in range(A.cols):
            for n in range(C.cols):
                C[m,n] += A[m,k] * B[k,n]

fn main():
    let M = 128
    let N = 128
    let K = 128
    
    var A = Matrix(M, K)
    var B = Matrix(K, N)
    var C = Matrix(M, N)
    
    # Initialize matrices
    for i in range(A.rows):
        for j in range(A.cols):
            A[i,j] = 1.0
    for i in range(B.rows):
        for j in range(B.cols):
            B[i,j] = 2.0
    
    # Perform matrix multiplication
    matmul(C, A, B)
    print(C[0,0])