; Hello World program for Z80 Assembly
; Outputs "Hello, World!" to the screen using CP/M BDOS calls

        ORG     0100H           ; CP/M programs start at 0100H

START:  LD      DE,MSG          ; Load address of message into DE
        LD      C,9             ; BDOS function 9: Print String
        CALL    0005H           ; Call BDOS
        RET                     ; Return to CP/M

MSG:    DB      'Hello, World!$'