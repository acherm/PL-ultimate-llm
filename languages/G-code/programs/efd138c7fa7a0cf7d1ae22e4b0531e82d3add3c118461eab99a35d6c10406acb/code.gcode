;Example one: simple linear movement
G90 ;absolute movement
G21 ;metric
G00 Z50.0 ;pen up
G00 X10 Y10 ;move to start position
G01 Z0 ;pen down
G01 X20 Y10 F100 ;line to 20,10 at 100 units/min
G01 X20 Y20 ;line to 20,20
G01 X10 Y20 ;line to 10,20
G01 X10 Y10 ;line to 10,10
G00 Z50 ;pen up
M02 ;end program