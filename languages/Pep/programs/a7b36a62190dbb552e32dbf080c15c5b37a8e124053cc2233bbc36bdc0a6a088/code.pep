         BR main
msg:    .ASCII "Hello, World!\n\x00"
main:   STRO msg,d
        STOP
        .END