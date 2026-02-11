* Simple Interest Calculator in PL/B
* Calculates simple interest from principal, rate, and time

START
    CLEAR
    DISPLAY "Simple Interest Calculator"
    DISPLAY "=========================="
    DISPLAY ""

    DISPLAY "Enter Principal Amount: "
    ACCEPT PRINCIPAL

    DISPLAY "Enter Interest Rate (%): "
    ACCEPT RATE

    DISPLAY "Enter Time (years): "
    ACCEPT TIME

    CALC INTEREST = (PRINCIPAL * RATE * TIME) / 100

    DISPLAY ""
    DISPLAY "Principal: ", PRINCIPAL
    DISPLAY "Rate: ", RATE, "%"
    DISPLAY "Time: ", TIME, " years"
    DISPLAY "Simple Interest: ", INTEREST

    STOP