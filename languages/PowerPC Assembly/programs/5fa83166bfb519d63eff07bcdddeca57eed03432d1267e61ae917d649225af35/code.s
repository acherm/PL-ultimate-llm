# PowerPC Assembly - Simple addition program
# Adds two numbers and stores result

.section .data
num1:   .long 5
num2:   .long 10
result: .long 0

.section .text
.globl _start

_start:
    # Load address of num1 into r3
    lis r3, num1@ha
    addi r3, r3, num1@l

    # Load num1 into r4
    lwz r4, 0(r3)

    # Load address of num2 into r5
    lis r5, num2@ha
    addi r5, r5, num2@l

    # Load num2 into r6
    lwz r6, 0(r5)

    # Add r4 and r6, store in r7
    add r7, r4, r6

    # Load address of result into r8
    lis r8, result@ha
    addi r8, r8, result@l

    # Store result
    stw r7, 0(r8)

    # Exit (syscall convention varies by OS)
    li r0, 1
    sc