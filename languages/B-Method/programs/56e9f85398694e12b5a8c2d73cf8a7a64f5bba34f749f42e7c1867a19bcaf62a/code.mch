MACHINE Cruise_finite1
/* A simple cruise controller */
SETS
  BUTTONS = {off, on, resume, brake, gas, acc}
CONSTANTS
  max_speed, min_speed
PROPERTIES
  max_speed = 120 & min_speed = 30 & max_speed > min_speed
VARIABLES
  speed, active, mem
INVARIANT
  speed : NATURAL &
  active : BOOL &
  mem : NATURAL &
  (active = TRUE => speed >= min_speed & speed <= max_speed) &
  mem >= min_speed & mem <= max_speed
INITIALISATION
  speed := 0 || active := FALSE || mem := min_speed
OPERATIONS
  press(button) = PRE button : BUTTONS THEN
    CHOICE
      button = off THEN active := FALSE
    OR
      button = on & active = FALSE & speed >= min_speed & speed <= max_speed THEN
        active := TRUE || mem := speed
    OR
      button = resume & active = FALSE & mem >= min_speed & mem <= max_speed THEN
        active := TRUE || speed := mem
    OR
      button = brake THEN
        active := FALSE
    OR
      button = gas & active = TRUE & speed < max_speed THEN
        speed := speed + 1
    OR
      button = acc & active = TRUE & speed < max_speed THEN
        speed := speed + 1 || mem := speed
    OR
      button : {on, resume, gas, acc} & /* no change of state */
      skip
    END
  END;

  time_step(s_change) = PRE s_change : -1..1 THEN
     IF active = FALSE & speed > 0 & s_change < 1 THEN
        speed := speed - 1
     ELSIF active = TRUE & speed+s_change >= min_speed & speed+s_change <= max_speed THEN
        speed := speed + s_change
     END
  END
END