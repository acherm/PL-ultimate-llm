# Simple RISC-V Assembly program to compute sum of first 10 numbers
# Result stored in register a0

.text
.globl _start

_start:
    li a0, 0        # Initialize sum to 0
    li a1, 1        # Initialize counter to 1
    li a2, 10       # Set limit to 10

loop:
    add a0, a0, a1  # Add counter to sum
    addi a1, a1, 1  # Increment counter
    ble a1, a2, loop # Branch if counter <= limit

    # Exit (syscall 93)
    li a7, 93       # Exit syscall number
    ecall           # Make syscall
