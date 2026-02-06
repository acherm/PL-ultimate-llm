BEGIN "Factorial"
    INTEGER PROCEDURE Factorial(N);
    INTEGER N;
    BEGIN
        IF N <= 1 THEN
            RETURN(1)
        ELSE
            RETURN(N * Factorial(N - 1));
    END;

    INTEGER I, Result;

    FOR I := 1 STEP 1 UNTIL 10 DO
    BEGIN
        Result := Factorial(I);
        PRINT(I, " factorial is ", Result);
    END;
END "Factorial";
