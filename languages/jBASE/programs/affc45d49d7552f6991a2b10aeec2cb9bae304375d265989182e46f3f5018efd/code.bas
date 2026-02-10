* Simple customer record management program in jBASE
* This program reads and displays customer information

PROGRAM CUSTOMER.DISPLAY

* Open the customer file
OPEN 'CUSTOMERS' TO F.CUSTOMERS ELSE
    CRT 'Cannot open CUSTOMERS file'
    STOP
END

* Get customer ID from user
CRT 'Enter Customer ID: ':
INPUT CUST.ID

* Read customer record
READ CUST.REC FROM F.CUSTOMERS, CUST.ID ELSE
    CRT 'Customer not found: ':CUST.ID
    STOP
END

* Extract fields from the record
CUST.NAME = CUST.REC<1>
CUST.ADDRESS = CUST.REC<2>
CUST.PHONE = CUST.REC<3>
CUST.BALANCE = CUST.REC<4>

* Display customer information
CRT
CRT 'Customer Information:'
CRT '===================='
CRT 'ID:      ':CUST.ID
CRT 'Name:    ':CUST.NAME
CRT 'Address: ':CUST.ADDRESS
CRT 'Phone:   ':CUST.PHONE
CRT 'Balance: ':CUST.BALANCE

* Close file
CLOSE F.CUSTOMERS

STOP
END