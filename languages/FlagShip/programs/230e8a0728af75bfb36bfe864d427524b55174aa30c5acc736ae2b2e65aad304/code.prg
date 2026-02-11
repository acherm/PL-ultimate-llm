* Simple Database Example in FlagShip
PROCEDURE Main
    LOCAL cName, nAge, lContinue

    ? "FlagShip Database Demo"
    ? STRING(40, "-")

    * Create and use a database
    CREATE TABLE customer (name C(30), age N(3), email C(50))
    USE customer

    lContinue = .T.
    DO WHILE lContinue
        CLEAR
        @ 1, 0 SAY "Enter customer name (blank to quit):"
        @ 2, 0 GET cName
        READ

        IF EMPTY(cName)
            lContinue = .F.
            LOOP
        ENDIF

        @ 4, 0 SAY "Enter age:"
        @ 5, 0 GET nAge
        READ

        * Add record
        APPEND BLANK
        REPLACE name WITH cName, age WITH nAge

        ? "Record added successfully!"
        WAIT
    ENDDO

    * Display all records
    CLEAR
    ? "All Customers:"
    ? STRING(40, "=")
    GO TOP
    DO WHILE !EOF()
        ? "Name:", TRIM(name), "Age:", age
        SKIP
    ENDDO

    CLOSE ALL
RETURN