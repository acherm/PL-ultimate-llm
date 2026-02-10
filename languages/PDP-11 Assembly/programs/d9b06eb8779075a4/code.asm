        .title  HELLO

        .global _start

_start:
        mov     $msg, r1
loop:
        movb    (r1)+, r0
        beq     done
        .trap   1               ; write character
        br      loop
done:
        .trap   0               ; exit

msg:    .ascii  "Hello, World!\n"
        .byte   0
