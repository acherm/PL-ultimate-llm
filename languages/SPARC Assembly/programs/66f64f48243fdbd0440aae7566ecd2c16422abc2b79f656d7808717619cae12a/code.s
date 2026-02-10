.section ".data"
msg:
    .asciz "Hello, World!\n"

.section ".text"
.global main
.align 4

main:
    save %sp, -96, %sp
    set msg, %o0
    call printf
    nop
    restore
    retl
    nop
