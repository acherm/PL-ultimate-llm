/*
** OpenROAD 4GL - Fibonacci sequence example
*/

INITIALIZE =
DECLARE
    ii    = INTEGER NOT NULL;
    a     = INTEGER NOT NULL;
    b     = INTEGER NOT NULL;
    tmp   = INTEGER NOT NULL;
    msg   = VARCHAR(500) NOT NULL;
BEGIN
    a   = 0;
    b   = 1;
    msg = '0, 1';

    FOR ii = 1 TO 8 DO
        tmp = a + b;
        a   = b;
        b   = tmp;
        msg = msg + ', ' + VARCHAR(b);
    ENDFOR;

    MESSAGE msg
    WITH STYLE = POPUP;
END
