to setup
  ca
  crt 100
  ask turtles [
    set color blue - 2
  ]
  reset-ticks
end

to go
  ask turtles [
    fd 1
  ]
  tick
end