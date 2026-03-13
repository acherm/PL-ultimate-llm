// Fibonacci sequence in CA-Visual Objects
// Displays first 10 Fibonacci numbers in a message box

FUNCTION Start()
    LOCAL nFirst  AS INT
    LOCAL nSecond AS INT
    LOCAL nTemp   AS INT
    LOCAL n       AS INT
    LOCAL cList   AS STRING

    nFirst  := 0
    nSecond := 1
    cList   := "Fibonacci Sequence:" + Chr(13) + Chr(10)

    FOR n := 1 TO 10
        cList   += NTrim(nFirst) + Chr(13) + Chr(10)
        nTemp   := nFirst + nSecond
        nFirst  := nSecond
        nSecond := nTemp
    NEXT

    MsgBox(cList, "Fibonacci Demo", MBOKONLY)
    RETURN NIL
