# RoboMind: Navigate a maze using the right-hand rule
# Demonstrates procedures, conditionals, and sensor commands

procedure turnAround() {
  right()
  right()
}

procedure step() {
  if rightIsClear() {
    right()
    forward(1)
  } else {
    if frontIsClear() {
      forward(1)
    } else {
      if leftIsClear() {
        left()
        forward(1)
      } else {
        turnAround()
      }
    }
  }
}

repeat 30 {
  step()
}
