; Hello World program in Pep/9
; Outputs "Hello, world!\n"

         BR      main
msg:     .ASCII  "Hello, world!\x00"

main:    LDBA    msg,d       ; Load byte from message
         CPBA    0,i         ; Compare with null terminator
         BREQ    done        ; If null, we're done
         STBA    charOut,d   ; Output character
         ADDA    1,i         ; Move to next character
         BR      main        ; Loop
done:    STOP
         .END