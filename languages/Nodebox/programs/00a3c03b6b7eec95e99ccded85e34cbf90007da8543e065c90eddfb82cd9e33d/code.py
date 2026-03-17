size(500, 500)
background(0.15, 0.15, 0.25)

nofill()
strokewidth(1)

translate(250, 250)

for i in range(0, 360, 5):
    stroke(i / 360.0, 1 - i / 360.0, 0.8, 0.6)
    push()
    rotate(i)
    translate(80, 0)
    oval(-15, -15, 30, 30)
    pop()
