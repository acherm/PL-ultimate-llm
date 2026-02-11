/ HELLO WORLD PROGRAM FOR PDP-15
/ USES TELEPRINTER OUTPUT

*200                    / START AT LOCATION 200
BEGIN,  LAW MSG         / LOAD ADDRESS OF MESSAGE
        DAC PTR         / STORE IN POINTER
LOOP,   LAC PTR I       / LOAD CHAR FROM MESSAGE
        SNA             / SKIP IF NON-ZERO
        HLT             / HALT IF ZERO
        TLS             / OUTPUT TO TELEPRINTER
        LAC PTR         / LOAD POINTER
        IAC             / INCREMENT
        DAC PTR         / STORE BACK
        JMP LOOP        / CONTINUE LOOP

PTR,    0
MSG,    110             / H
        105             / E
        114             / L
        114             / L
        117             / O
        040             / SPACE
        127             / W
        117             / O
        122             / R
        114             / L
        104             / D
        012             / NEWLINE
        0               / TERMINATOR

$BEGIN                  / SET START ADDRESS