// Simple launch autopilot for Kerbal Space Program
// Launches a rocket to orbit

CLEARSCREEN.
SET TARGET_ALTITUDE TO 80000.
SET TARGET_APOAPSIS TO 100000.

PRINT "Launch sequence initiated".
PRINT "Target altitude: " + TARGET_ALTITUDE.

// Stage countdown
FROM {local countdown is 5.} UNTIL countdown = 0 STEP {SET countdown to countdown - 1.} DO {
    PRINT "T-" + countdown.
    WAIT 1.
}

// Launch
PRINT "Liftoff!".
STAGE.
LOCK THROTTLE TO 1.0.
LOCK STEERING TO HEADING(90, 90).

// Ascent phase
WAIT UNTIL SHIP:ALTITUDE > 100.
PRINT "Beginning gravity turn".

LOCK STEERING TO HEADING(90, 90 - (SHIP:ALTITUDE / TARGET_ALTITUDE * 45)).

// Stage when out of fuel
WHEN STAGE:SOLIDFUEL < 0.1 THEN {
    PRINT "Staging".
    STAGE.
    PRESERVE.
}

// Coast to apoapsis
WAIT UNTIL SHIP:APOAPSIS > TARGET_APOAPSIS.
LOCK THROTTLE TO 0.0.
PRINT "Target apoapsis reached".
PRINT "Mission complete".
