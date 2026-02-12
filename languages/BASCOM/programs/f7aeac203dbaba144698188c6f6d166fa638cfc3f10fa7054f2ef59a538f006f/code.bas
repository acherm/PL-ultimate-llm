'LED Blink Program for ATmega328P
'Blinks an LED connected to PORTB.0

$regfile = "m328pdef.dat"
$crystal = 16000000
$hwstack = 40
$swstack = 16
$framesize = 32

Config Portb.0 = Output

Do
   Portb.0 = 1
   Waitms 500
   Portb.0 = 0
   Waitms 500
Loop

End
