DECLARE SUB BubbleSort (arr() AS INTEGER, n AS INTEGER)

DIM numbers(9) AS INTEGER
DIM i AS INTEGER

DATA 64, 25, 12, 22, 11, 90, 3, 47, 8, 56

FOR i = 0 TO 9
    READ numbers(i)
NEXT i

CALL BubbleSort(numbers(), 10)

PRINT "Sorted numbers:"
FOR i = 0 TO 9
    PRINT numbers(i);
NEXT i
PRINT

END

SUB BubbleSort (arr() AS INTEGER, n AS INTEGER)
    DIM i AS INTEGER, j AS INTEGER, temp AS INTEGER
    FOR i = 0 TO n - 2
        FOR j = 0 TO n - i - 2
            IF arr(j) > arr(j + 1) THEN
                temp = arr(j)
                arr(j) = arr(j + 1)
                arr(j + 1) = temp
            END IF
        NEXT j
    NEXT i
END SUB
