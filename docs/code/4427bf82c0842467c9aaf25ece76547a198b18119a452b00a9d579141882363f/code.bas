SCREEN 12
CLS
FOR i = 1 TO 200
    x = INT(RND * 640)
    y = INT(RND * 480)
    c = INT(RND * 15) + 1
    PSET (x, y), c
NEXT i
FOR angle = 0 TO 360 STEP 5
    x1 = 320 + 200 * COS(angle * 3.14159 / 180)
    y1 = 240 + 200 * SIN(angle * 3.14159 / 180)
    LINE (320, 240)-(x1, y1), angle MOD 15 + 1
NEXT angle
DO: LOOP WHILE INKEY$ = ""
