        .title  "Simple Addition Example"
        .text

start:
        ; Load first value into accumulator
        LD      #100, A

        ; Add second value
        ADD     #50, A

        ; Store result
        STL     A, result

        ; Halt
        B       start

        .data
result: .word   0
        .end
