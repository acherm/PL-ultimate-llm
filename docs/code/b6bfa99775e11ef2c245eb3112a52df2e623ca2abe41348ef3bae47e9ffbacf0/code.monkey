Import mojo

Class Player
	Field x:Float
	Field y:Float
	Field speed:Float = 4.0
	Field jumping:Bool
	Field gravity:Float = 0.5
	Field velocity:Float = 0.0
	
	Method New(x:Float, y:Float)
		Self.x = x
		Self.y = y
	End
	
	Method Update()
		If KeyDown(KEY_LEFT) Then x -= speed
		If KeyDown(KEY_RIGHT) Then x += speed
		
		If KeyHit(KEY_SPACE) And Not jumping
			velocity = -12.0
			jumping = True
		EndIf
		
		velocity += gravity
		y += velocity
		
		If y > 400
			y = 400
			velocity = 0
			jumping = False
		EndIf
	End
	
	Method Draw()
		DrawRect x, y, 32, 32
	End
End

Class MyGame Extends App
	Field player:Player
	
	Method OnCreate()
		player = New Player(100, 100)
	End
	
	Method OnUpdate()
		player.Update()
	End
	
	Method OnRender()
		Cls
		player.Draw()
	End
End

Function Main()
	New MyGame
End