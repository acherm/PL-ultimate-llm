section .data
    hello db 'Hello, World!',0
section .text
    global _start
_start:
    ; write our string to stdout
    mov rax, 1          ; syscall: write
    mov rdi, 1          ; file descriptor: stdout
    mov rsi, hello      ; pointer to string
    mov rdx, 13         ; length of string
    syscall              ; invoke operating system to do the write
    ; exit
    mov rax, 60         ; syscall: exit
    xor rdi, rdi        ; exit code 0
    syscall