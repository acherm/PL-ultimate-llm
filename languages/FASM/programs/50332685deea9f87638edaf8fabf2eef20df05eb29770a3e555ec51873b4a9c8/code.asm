format ELF64 executable 3
entry start

segment readable executable
start:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg
    mov rdx, msg_len
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall

segment readable writeable
msg db 'Hello, World!', 0xA
msg_len = $ - msg
