* FoxBASE program to create and populate a customer database
CLEAR
SET TALK OFF

* Create database structure
CREATE customers
USE customers
APPEND BLANK
REPLACE name WITH "John Smith", city WITH "New York", balance WITH 1500.00
APPEND BLANK
REPLACE name WITH "Jane Doe", city WITH "Los Angeles", balance WITH 2300.50
APPEND BLANK
REPLACE name WITH "Bob Johnson", city WITH "Chicago", balance WITH 875.25

* Display all records
GO TOP
LIST

* Find customers with balance > 1000
? "Customers with balance over $1000:"
GO TOP
DO WHILE .NOT. EOF()
    IF balance > 1000
        ? name, balance
    ENDIF
    SKIP
ENDDO

CLOSE ALL
QUIT