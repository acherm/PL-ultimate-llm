Scriptname HelloWorldScript extends ObjectReference

Event OnActivate(ObjectReference akActionRef)
    Debug.MessageBox("Hello, World!")
    Debug.Notification("You activated " + GetDisplayName())

    int count = 0
    while count < 5
        count += 1
        Debug.Trace("Count is: " + count)
    endWhile

    if akActionRef == Game.GetPlayer()
        Debug.Notification("Activated by the player")
    else
        Debug.Notification("Activated by an NPC")
    endIf
endEvent
