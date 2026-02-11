        .text
        .globl main
        .ent main
main:
        ldgp    $gp, 0($27)
        lda     $sp, -16($sp)
        stq     $26, 0($sp)

        # Compute Fibonacci(10)
        lda     $16, 10
        bsr     $26, fib

        # Result is in $0
        mov     $0, $16
        ldq     $26, 0($sp)
        lda     $sp, 16($sp)
        ret     $31, ($26), 1
        .end main

        .ent fib
fib:
        lda     $sp, -32($sp)
        stq     $26, 0($sp)
        stq     $9, 8($sp)
        stq     $10, 16($sp)

        # Base case: if n <= 1, return n
        cmpule  $16, 1, $1
        beq     $1, fib_recurse
        mov     $16, $0
        br      fib_return

fib_recurse:
        # Save n
        mov     $16, $9

        # Compute fib(n-1)
        subq    $16, 1, $16
        bsr     $26, fib
        mov     $0, $10

        # Compute fib(n-2)
        subq    $9, 2, $16
        bsr     $26, fib

        # Return fib(n-1) + fib(n-2)
        addq    $10, $0, $0

fib_return:
        ldq     $10, 16($sp)
        ldq     $9, 8($sp)
        ldq     $26, 0($sp)
        lda     $sp, 32($sp)
        ret     $31, ($26), 1
        .end fib
