Graphics 640,480,0,1
SetBuffer BackBuffer()

x = 320
y = 240

While Not KeyDown(1)
    Cls

    If KeyDown(203) Then x = x - 2
    If KeyDown(205) Then x = x + 2
    If KeyDown(200) Then y = y - 2
    If KeyDown(208) Then y = y + 2

    Color 255,0,0
    Oval x-10, y-10, 20, 20, 1

    Color 255,255,255
    Text 10, 10, "Use arrow keys to move. ESC to quit."

    Flip
Wend

End
