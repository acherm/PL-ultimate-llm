; Simple addition program for PEP-10
; Adds two numbers and stores the result

         BR      main        ; Branch to main program
num1:    .WORD   5          ; First number
num2:    .WORD   3          ; Second number
result:  .BLOCK  2          ; Space for result

main:    LDWA    num1,d     ; Load first number
         ADDA    num2,d     ; Add second number
         STWA    result,d   ; Store result
         STOP               ; Halt execution
         .END
