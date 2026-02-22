BEGIN
  WHILE not-facing-west DO turnleft
  WHILE front-is-clear DO move
  turnleft turnleft turnleft
  WHILE front-is-clear DO move
  turnleft turnleft turnleft
  WHILE left-is-blocked DO move
  turnleft move move
  WHILE not-next-to-a-beeper DO move
  pickbeeper turnleft move move
  putbeeper move
  turnoff
END
