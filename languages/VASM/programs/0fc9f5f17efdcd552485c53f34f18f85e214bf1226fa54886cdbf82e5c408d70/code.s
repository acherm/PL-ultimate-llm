; Simple M68k assembly program for VASM
; Prints "Hello" to console

        section code

start:
        move.l  #message,-(sp)  ; Push message address
        move.w  #9,-(sp)        ; DOS function 9 (write string)
        trap    #1              ; Call DOS
        addq.l  #6,sp           ; Clean up stack
        
        move.w  #0,-(sp)        ; Exit code 0
        trap    #1              ; Exit

        section data

message:
        dc.b    'Hello, VASM!',13,10,'$'
