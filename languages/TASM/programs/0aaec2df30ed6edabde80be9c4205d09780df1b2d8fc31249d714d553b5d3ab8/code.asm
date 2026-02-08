.MODEL SMALL
.STACK 100h

.DATA
    message DB 'Hello, World!$'

.CODE
main PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV AH, 09h
    LEA DX, message
    INT 21h

    MOV AH, 4Ch
    INT 21h
main ENDP
END main