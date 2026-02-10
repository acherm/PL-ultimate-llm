* Hello World in Motorola 68000 Assembly
* For the Sinclair QL computer

        section .text
        global  _start

_start:
        move.l  #message,a1     ; Address of message
        move.w  #13,d1          ; Length of message
        moveq   #2,d0           ; TRAP #1, function 2 (write string)
        trap    #1

        moveq   #0,d0           ; Exit code 0
        trap    #1              ; TRAP #1, exit

        section .data
message:
        dc.b    'Hello, World!',10