{
  Simple "Hello World" program in SPIN
}

CON
  _clkmode = xtal1 + pll16x       
  _xinfreq = 80_000_000

OBJ
  pst : "Parallax Serial Terminal"

PUB start | i
  pst.start(115_200)              'start with serial terminal (optional)
  repeat i from 0 to 39            'send 40 characters
    pst.char("Hello World! #" .+ i => 32)
  pst.str(string("\n"))
  repeat                          'hang until power off or reset