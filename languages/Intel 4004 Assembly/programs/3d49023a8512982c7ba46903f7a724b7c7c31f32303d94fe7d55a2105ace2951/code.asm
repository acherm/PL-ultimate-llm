; Intel 4004 Assembly - Simple addition program
; Adds two numbers and stores the result

        FIM 0, 5        ; Load register pair 0 with immediate value 5
        FIM 1, 3        ; Load register pair 1 with immediate value 3
        SRC 0           ; Set ROM/RAM address from register pair 0
        LDM 5           ; Load accumulator with immediate value 5
        XCH R2          ; Exchange accumulator with register 2
        LDM 3           ; Load accumulator with immediate value 3
        ADD R2          ; Add register 2 to accumulator
        XCH R3          ; Store result in register 3
        END             ; End of program
