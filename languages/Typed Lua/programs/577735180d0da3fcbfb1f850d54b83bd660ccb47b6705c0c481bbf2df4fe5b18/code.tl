local interface Shape
  area: (number) -> number
  perimeter: (number) -> number
end

local interface Circle
  radius: number
end

local function circle_area(radius: number): number
  return 3.14159 * radius * radius
end

local function circle_perimeter(radius: number): number
  return 2 * 3.14159 * radius
end

local r: number = 5
print('Circle with radius ' .. r)
print('Area: ' .. circle_area(r))
print('Perimeter: ' .. circle_perimeter(r))
