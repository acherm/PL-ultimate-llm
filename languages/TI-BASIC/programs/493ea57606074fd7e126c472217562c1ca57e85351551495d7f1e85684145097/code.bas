:ClrHome
:For(I,2,99)
:0→F
:For(J,2,I-1)
:If not(fPart(I/J))
:1→F
:End
:If F=0
:Disp I
:End
:End
:Pause