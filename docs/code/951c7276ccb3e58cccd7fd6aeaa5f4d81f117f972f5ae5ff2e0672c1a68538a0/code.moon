class Vec2
  new: (@x, @y) =>
  __tostring: -> "Vec2(#{@x}, #{@y})"
  +: (other) => Vec2 @x + other.x, @y + other.y

v = Vec2 10, 20
print tostring v