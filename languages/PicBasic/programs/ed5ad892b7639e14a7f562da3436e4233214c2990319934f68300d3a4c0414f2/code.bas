' PicBasic LED Blinker
' Blinks an LED connected to PORTB.0

DEFINE OSC 4

led VAR PORTB.0

TRISB = %00000000  ' Set PORTB as outputs

loop:
    HIGH led       ' Turn LED on
    PAUSE 500      ' Wait 0.5 seconds
    LOW led        ' Turn LED off
    PAUSE 500      ' Wait 0.5 seconds
    GOTO loop      ' Repeat

END
