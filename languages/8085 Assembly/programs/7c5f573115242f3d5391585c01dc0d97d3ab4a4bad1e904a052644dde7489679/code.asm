        MVI A, 05H      ; Load 5 into accumulator
        MVI B, 03H      ; Load 3 into register B
        ADD B           ; Add B to accumulator
        STA 2050H       ; Store result at memory location 2050H
        HLT             ; Halt the program