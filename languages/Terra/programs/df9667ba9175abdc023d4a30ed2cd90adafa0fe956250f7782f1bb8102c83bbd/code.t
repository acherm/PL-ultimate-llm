local terralib = require "terra"

local printf = terralib.includecstring "stdio.h"

terra hello()
  printf("Hello, world!\n")
end

hello:entry()