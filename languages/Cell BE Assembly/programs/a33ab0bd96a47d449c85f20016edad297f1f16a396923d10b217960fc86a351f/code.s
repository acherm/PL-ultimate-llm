# SPU Assembly - Vector Addition
# Adds two vectors and stores result
# Origin: IBM Cell BE Programming Handbook examples

.data
vec_a:  .word 1, 2, 3, 4
vec_b:  .word 5, 6, 7, 8
result: .space 16

.text
.global _start
_start:
    # Load address of vec_a into r3
    ila     r3, vec_a
    # Load vector a into r4
    lqd     r4, 0(r3)

    # Load address of vec_b into r5
    ila     r5, vec_b
    # Load vector b into r6
    lqd     r6, 0(r5)

    # Add vectors: r7 = r4 + r6
    a       r7, r4, r6

    # Load address of result into r8
    ila     r8, result
    # Store result
    stqd    r7, 0(r8)

    # Stop the SPU
    stop    0x2000
