       IDENTIFICATION DIVISION.
       PROGRAM-ID. DLISAMP.
      *
      * DL/I Sample: Retrieve a customer segment from IMS database
      * Demonstrates GU (Get Unique) and GN (Get Next) DL/I calls
      *
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  DLI-FUNCTIONS.
           05  GU-FUNC       PIC X(4)  VALUE 'GU  '.
           05  GN-FUNC       PIC X(4)  VALUE 'GN  '.
           05  ISRT-FUNC     PIC X(4)  VALUE 'ISRT'.
       01  UNQUALIFIED-SSA   PIC X(9)  VALUE 'CUSTOMER*'.
       01  QUALIFIED-SSA.
           05  SSA-SEGMENT   PIC X(8)  VALUE 'CUSTOMER'.
           05  FILLER        PIC X     VALUE '('.
           05  SSA-FIELD     PIC X(8)  VALUE 'CUSTNO  '.
           05  SSA-RELOPER   PIC X(2)  VALUE '= '.
           05  SSA-VALUE     PIC X(8)  VALUE '00001234'.
           05  FILLER        PIC X     VALUE ')'.
       01  CUSTOMER-SEGMENT.
           05  CUST-NUMBER   PIC X(8).
           05  CUST-NAME     PIC X(30).
           05  CUST-ADDR     PIC X(40).
       LINKAGE SECTION.
       01  PCB-MASK.
           05  DBD-NAME      PIC X(8).
           05  SEGMENT-LEVEL PIC X(2).
           05  STATUS-CODE   PIC X(2).
           05  PROC-OPTIONS  PIC X(4).
           05  RESERVED      PIC S9(5) COMP.
           05  SEGMENT-NAME  PIC X(8).
           05  KEY-LEN       PIC S9(5) COMP.
           05  SENSEG-COUNT  PIC S9(5) COMP.
           05  KEY-AREA      PIC X(11).
       PROCEDURE DIVISION.
      * Perform a GU (Get Unique) call to retrieve specific customer
           CALL 'CBLTDLI' USING GU-FUNC
                                PCB-MASK
                                CUSTOMER-SEGMENT
                                QUALIFIED-SSA.
           EVALUATE STATUS-CODE
               WHEN SPACES
                   DISPLAY 'FOUND: ' CUST-NUMBER ' ' CUST-NAME
               WHEN 'GE'
                   DISPLAY 'CUSTOMER 00001234 NOT FOUND'
               WHEN OTHER
                   DISPLAY 'DL/I ERROR STATUS: ' STATUS-CODE
                   STOP RUN
           END-EVALUATE.
      * Perform GN (Get Next) calls to scan remaining segments
           PERFORM UNTIL STATUS-CODE = 'GB'
               CALL 'CBLTDLI' USING GN-FUNC
                                    PCB-MASK
                                    CUSTOMER-SEGMENT
                                    UNQUALIFIED-SSA
               IF STATUS-CODE = SPACES
                   DISPLAY 'NEXT: ' CUST-NUMBER ' ' CUST-NAME
               END-IF
           END-PERFORM.
           STOP RUN.
