        ORG     $0100
START   LDX     #MSG        Load address of message
LOOP    LDAA    0,X         Load character
        BEQ     DONE        If zero, we're done
        JSR     $E1D1       Call MIKBUG OUTCH routine
        INX                 Next character
        BRA     LOOP        Continue loop
DONE    SWI                 Return to monitor

MSG     FCC     "Hello, World!"
        FCB     $0D,$0A     Carriage return, line feed
        FCB     $00         Null terminator