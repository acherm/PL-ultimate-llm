; Hello World in x86-64 Assembly (NASM syntax, Linux)
section .data
    msg     db  'Hello, World!', 0x0a
    msglen  equ $ - msg

section .text
    global _start

_start:
    mov     rax, 1          ; sys_write
    mov     rdi, 1          ; stdout (fd=1)
    mov     rsi, msg        ; buffer address
    mov     rdx, msglen     ; buffer length
    syscall

    mov     rax, 60         ; sys_exit
    xor     rdi, rdi        ; exit code 0
    syscall
