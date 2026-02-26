format ELF executable
entry _start

segment readable executable

_start:
        mov     eax, 4
        mov     ebx, 1
        mov     ecx, msg
        mov     edx, msglen
        int     0x80

        mov     eax, 1
        xor     ebx, ebx
        int     0x80

segment readable writeable

msg     db      'Hello, World!', 10
msglen = $ - msg
