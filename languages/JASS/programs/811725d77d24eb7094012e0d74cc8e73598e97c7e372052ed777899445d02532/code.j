// Simple JASS function to display a message
function HelloWorld takes nothing returns nothing
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Hello, World!")
endfunction

// Initialize function called when map starts
function InitTrig_HelloWorld takes nothing returns nothing
    local trigger t = CreateTrigger()
    call TriggerRegisterTimerEvent(t, 0.00, false)
    call TriggerAddAction(t, function HelloWorld)
endfunction