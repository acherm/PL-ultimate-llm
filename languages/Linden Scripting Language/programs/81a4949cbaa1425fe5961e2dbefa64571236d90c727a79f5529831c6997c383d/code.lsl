// Simple Door Script
// by F-Script
//
// Put this script in a prim, and it will become a simple door.
// The door will swing on the Z axis.
// It will open when touched, and close itself after a few seconds.

// The number of seconds the door will stay open.
float openTime = 3.0;

// The angle (in degrees) the door will swing open.
float swing = 90.0;

// These are used by the script. You don't need to change them.
integer doorState = FALSE; // FALSE = closed, TRUE = open
rotation rotClosed;
rotation rotOpen;

default
{
    state_entry()
    {
        // When the script starts, it will figure out the open and closed rotations.
        // It assumes the door is closed when the script is first run.
        rotClosed = llGetLocalRot();
        rotOpen = rotClosed * llEuler2Rot(0, 0, swing * DEG_TO_RAD);
    }

    touch_start(integer total_number)
    {
        // When touched, toggle the door's state.
        if (doorState == FALSE)
        {
            // It's closed, so open it.
            doorState = TRUE;
            llSetRot(rotOpen);
            llSetTimerEvent(openTime);
        }
        else
        {
            // It's open, so close it.
            doorState = FALSE;
            llSetRot(rotClosed);
            llSetTimerEvent(0); // Turn off the timer.
        }
    }

    timer()
    {
        // When the timer goes off, it means the door has been open long enough.
        // So, we close it.
        doorState = FALSE;
        llSetRot(rotClosed);
        llSetTimerEvent(0); // Turn off the timer.
    }
}