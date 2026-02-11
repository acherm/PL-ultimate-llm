        ; Simple PDP-6 Assembly program to add two numbers
        MOVE 1,NUM1     ; Load first number into register 1
        ADD 1,NUM2      ; Add second number to register 1
        MOVEM 1,RESULT  ; Store result in memory
        HALT            ; Stop execution

NUM1:   10              ; First number
NUM2:   20              ; Second number
RESULT: 0               ; Result storage
