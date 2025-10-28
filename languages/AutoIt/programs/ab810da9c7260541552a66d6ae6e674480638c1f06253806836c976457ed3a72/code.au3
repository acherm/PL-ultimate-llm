; Press Esc to terminate script, Pause/Break to "pause"
Global $Paused
HotKeySet("{PAUSE}", "TogglePause")
HotKeySet("{ESC}", "Terminate")
HotKeySet("{+!d}", "ShowMessage") ; Shift-Alt-d

;;;;;;;;

$Paused = False
While 1
    Sleep(100)
    ToolTip('Script is running...',0,0)
WEnd

Func TogglePause()
    $Paused = NOT $Paused
    While $Paused
        sleep(100)
        ToolTip('Script is paused...',0,0)
    WEnd
    ToolTip("")
EndFunc

Func Terminate()
    Exit 0
EndFunc

Func ShowMessage()
    MsgBox(4096,"My Script", "This is a message.")
EndFunc