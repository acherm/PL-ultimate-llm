        .LEVEL 2.0
        .SPACE $TEXT$
        .SUBSPA $CODE$

main
        .PROC
        .CALLINFO FRAME=0,NO_CALLS
        .ENTRY

        ; Add two numbers
        LDI     10,%r20         ; Load immediate 10 into r20
        LDI     20,%r21         ; Load immediate 20 into r21
        ADD     %r20,%r21,%r22  ; Add r20 and r21, store in r22

        ; Exit
        LDI     0,%r28          ; Return code 0
        BV      %r0(%rp)        ; Branch to return pointer
        NOP

        .EXIT
        .PROCEND
        .EXPORT main,ENTRY,PRIV_LEV=3
