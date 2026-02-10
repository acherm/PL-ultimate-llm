section .data
    msg db 'Hello, World!', 0x0A
    len equ $ - msg

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov eax, 4          ; sys_write
    mov ebx, 1          ; stdout
    mov ecx, msg        ; message to write
    mov edx, len        ; message length
    int 0x80            ; syscall

    ; exit(0)
    mov eax, 1          ; sys_exit
    xor ebx, ebx        ; exit code 0
    int 0x80            ; syscall
