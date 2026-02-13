BR      main
msg:    .ASCII  "Hello, world!\x00"
main:   LDWA    msg,i
        STRO    msg,d
        STOP
        .END
