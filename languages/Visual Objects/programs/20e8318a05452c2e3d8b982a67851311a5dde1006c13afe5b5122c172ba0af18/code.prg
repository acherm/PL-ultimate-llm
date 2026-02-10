CLASS HelloWorld
METHOD Init() CLASS HelloWorld
    SUPER:Init()
    RETURN SELF

METHOD Start() CLASS HelloWorld
    Alert("Hello, World!")
    RETURN SELF
END CLASS

FUNCTION Start()
    LOCAL oApp AS HelloWorld
    oApp := HelloWorld{}
    oApp:Start()
    RETURN NIL
