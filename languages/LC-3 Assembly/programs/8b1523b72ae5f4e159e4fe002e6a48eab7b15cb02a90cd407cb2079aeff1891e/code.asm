; LC-3 Hello World Program
; Demonstrates string output using TRAP x22 (PUTS)
        .ORIG x3000

        ; Load address of string into R0, then call PUTS
        LEA R0, HELLO_MSG   ; R0 <- address of string
        PUTS                ; TRAP x22: output null-terminated string
        HALT                ; TRAP x25: halt the machine

HELLO_MSG .STRINGZ "Hello, World!"
        .END