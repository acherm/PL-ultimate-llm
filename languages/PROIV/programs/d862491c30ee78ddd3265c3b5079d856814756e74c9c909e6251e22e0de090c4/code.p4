GLOBAL FUNCTION Example
    DISPLAY "Welcome to PROIV Programming"

    DECLARE NUMERIC nCounter
    DECLARE TEXT sMessage

    SET nCounter = 0

    WHILE nCounter < 10
        SET sMessage = "Count: " + STR(nCounter)
        DISPLAY sMessage
        SET nCounter = nCounter + 1
    ENDWHILE

    DISPLAY "Program completed successfully"

    RETURN
ENDFUNCTION
