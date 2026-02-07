; Rotating Cube in Blitz3D
Graphics3D 640, 480

camera = CreateCamera()
PositionEntity camera, 0, 0, -5

light = CreateLight()
RotateEntity light, 45, 45, 0

cube = CreateCube()

While Not KeyHit(1)
    RotateEntity cube, 0.5, 1.0, 0.3
    RenderWorld
    Flip
Wend

End