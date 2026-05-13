sr        =         44100
kr        =         4410
ksmps     =         10
nchnls    =         1

			instr 	901
inotedur	=		p3
imaxamp		=		ampdb(88)
icarrfreq	=		80
imodfreq	=		55
ilowndx		=		0
indxdiff	=		5-0

; PARAMETERS DEFINING THE ADSR AMPLITUDE ENVELOPE
; TIMES ARE A PERCENTAGE OF p3
;   attack amp  = p9     attack length  = p14
;   decay amp   = p10    decay length   = p15
;   sustain amp = p11    sustain length = p16
;   release amp = p12    release length = p17
;   end amp     = p13

; PARAMETERS DEFINING THE ADSR FREQ DEVIATION ENVELOPE
; TIMES ARE A PERCENTAGE OF p3
;   attack amp  = p18    attack length  = p23
;   decay amp   = p19    decay length   = p24
;   sustain amp = p20    sustain length = p25
;   release amp = p21    release length = p26
;   end amp     = p22

aampenv		linseg	.75, .125*p3, .8, .125*p3, 1.0, .25*p3, .15, .5*p3, .0
adevenv		linseg	1.0, .125*p3, .0, .25*p3, .0, .25*p3, .0, .25*p3, .0
amodosc		oscili	(ilowndx+indxdiff*adevenv)*imodfreq, imodfreq, 1
acarosc		oscili	imaxamp*aampenv, icarrfreq+amodosc, 1
			out		acarosc
			endin
