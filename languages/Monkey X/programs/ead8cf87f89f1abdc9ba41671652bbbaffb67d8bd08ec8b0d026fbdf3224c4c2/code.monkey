' Simple Monkey X example - Moving sprite
Import mojo

Class MyApp Extends App
    Field x:Float = 0
    Field y:Float = 0
    Field dx:Float = 2
    
    Method OnCreate:Int()
        SetUpdateRate(60)
        Return 0
    End
    
    Method OnUpdate:Int()
        x += dx
        If x > 640 Or x < 0 Then dx = -dx
        Return 0
    End
    
    Method OnRender:Int()
        Cls(0, 0, 0)
        SetColor(255, 255, 255)
        DrawCircle(x, y + 240, 20)
        Return 0
    End
End

Function Main:Int()
    New MyApp()
    Return 0
End