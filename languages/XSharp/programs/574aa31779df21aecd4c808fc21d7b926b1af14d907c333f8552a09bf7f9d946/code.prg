FUNCTION Start() AS VOID
    ? "Hello, World!"
    LOCAL nCount AS INT
    nCount := 10
    FOR VAR i := 1 TO nCount
        ? "Count: " + i:ToString()
    NEXT
    RETURN
