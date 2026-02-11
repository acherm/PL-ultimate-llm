/*
  99 bottles of beer
  Clipper 5.2
*/

procedure main

  local i

  for i = 99 to 1 step -1
    ? bottles( i ) + " of beer on the wall, " + bottles( i ) + " of beer."
    ? "Take one down and pass it around, " + bottles( i - 1 ) + " of beer on the wall."
    ?
  next

  return

function bottles( n )

  local cBottles := ""

  if n > 1
    cBottles = alltrim( str( n ) ) + " bottles"
  elseif n = 1
    cBottles = "1 bottle"
  else
    cBottles = "no more bottles"
  endif

  return cBottles