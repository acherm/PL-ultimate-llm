InputBox, MyVariable, My Title, Please enter a value
if ErrorLevel
    MsgBox, You pressed cancel.
else if MyVariable =
    MsgBox, You entered an empty value.
else
    MsgBox, You entered %MyVariable%.