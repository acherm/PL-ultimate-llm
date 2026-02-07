SCREEN 12
CLS
FOR i = 1 TO 100
    x1 = INT(RND * 640)
    y1 = INT(RND * 480)
    x2 = INT(RND * 640)
    y2 = INT(RND * 480)
    c = INT(RND * 15) + 1
    LINE (x1, y1)-(x2, y2), c
NEXT i
LOCATE 1, 1
PRINT "Press any key to exit"
SLEEP