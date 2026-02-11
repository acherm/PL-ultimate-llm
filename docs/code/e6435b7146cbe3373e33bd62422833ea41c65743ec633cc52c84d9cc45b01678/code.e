-> Shapes.e
->
-> A simple example of E's OOP features.
->
-> Compile with: ec Shapes.e

MODULE 'console'

OBJECT shape
   x, y
METHODS
   NEW(nx, ny)
   PROC draw()
ENDOBJECT

OBJECT circle ISA shape
   radius
METHODS
   NEW(nx, ny, nradius)
   PROC draw()
ENDOBJECT

OBJECT rectangle ISA shape
   width, height
METHODS
   NEW(nx, ny, nwidth, nheight)
   PROC draw()
ENDOBJECT

PROC main()
   DEF s:PTR TO shape, c:PTR TO circle, r:PTR TO rectangle
   s := NEW shape(10, 20)
   c := NEW circle(30, 40, 5)
   r := NEW rectangle(50, 60, 15, 8)
   s.draw()
   c.draw()
   r.draw()
   DisposeLink(s)
   DisposeLink(c)
   DisposeLink(r)
ENDPROC

METHOD shape.NEW(nx, ny)
   x := nx
   y := ny
ENDMETHOD

METHOD shape.draw()
   WriteF('Drawing a shape at (\d, \d)\n', x, y)
ENDMETHOD

METHOD circle.NEW(nx, ny, nradius)
   super.NEW(nx, ny)
   radius := nradius
ENDMETHOD

METHOD circle.draw()
   super.draw()
   WriteF('  It''s a circle with radius \d\n', radius)
ENDMETHOD

METHOD rectangle.NEW(nx, ny, nwidth, nheight)
   super.NEW(nx, ny)
   width := nwidth
   height := nheight
ENDMETHOD

METHOD rectangle.draw()
   super.draw()
   WriteF('  It''s a rectangle with width \d and height \d\n', width, height)
ENDMETHOD