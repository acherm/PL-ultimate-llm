; Hello World in 8086 Assembly
; Uses DOS interrupt 21h for output

.MODEL SMALL
.STACK 100h
.DATA
    msg DB 'Hello, World!$'
.CODE
main PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV AH, 09h         ; DOS function to display string
    LEA DX, msg         ; Load address of message
    INT 21h             ; Call DOS interrupt

    MOV AH, 4Ch         ; DOS function to terminate
    INT 21h             ; Call DOS interrupt
main ENDP
END main
