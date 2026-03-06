// Hello World in TNT Basic
// Demonstrates basic TNT Basic graphics and input

SetGraphicsMode(640, 480, 32, false)
SetCaption("Hello, TNT Basic!")

ClearScreen("white")
DrawText("Hello, World!", 200, 220, "Monaco", 28, "black")
DrawText("Click to quit.", 220, 260, "Monaco", 18, "gray")

repeat
until Button()

QuitProgram()
