-- Create a teapot with custom properties
teapotObj = Teapot()
teapotObj.radius = 50
teapotObj.segments = 4
teapotObj.pos = [0, 0, 0]
teapotObj.wirecolor = color 255 0 0

-- Create a sphere
sphereObj = Sphere()
sphereObj.radius = 30
sphereObj.segments = 32
sphereObj.pos = [100, 0, 0]
sphereObj.wirecolor = color 0 255 0

-- Print information
format "Created teapot at: %\n" teapotObj.pos
format "Created sphere at: %\n" sphereObj.pos
