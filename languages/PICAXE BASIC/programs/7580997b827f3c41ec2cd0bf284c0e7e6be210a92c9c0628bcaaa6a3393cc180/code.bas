' LED Blink Program for PICAXE
' Blinks an LED connected to output pin 0

main:
    high 0          ' Turn LED on
    pause 1000      ' Wait 1 second
    low 0           ' Turn LED off
    pause 1000      ' Wait 1 second
    goto main       ' Loop forever
