// Hello World program in IA-64 Assembly
// Based on standard IA-64 calling conventions

        .text
        .align 16
        .global _start
        .proc _start
_start:
        // Allocate stack frame
        alloc r2 = ar.pfs, 0, 0, 1, 0

        // Load address of message string
        addl r14 = @ltoffx(message), r1
        ld8.mov r14 = [r14], message

        // Set up write syscall (sys_write = 1)
        mov r15 = 1        // syscall number
        mov out0 = 1       // file descriptor (stdout)
        mov out1 = r14     // buffer address
        mov out2 = 14      // count (message length)

        // Make syscall
        break 0x100000

        // Exit program (sys_exit = 60)
        mov r15 = 60       // syscall number
        mov out0 = 0       // exit code
        break 0x100000

        .endp _start

        .data
message:
        .string "Hello, World!\n"
