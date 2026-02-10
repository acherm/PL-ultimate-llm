local fn SieveOfEratosthenes( limit as long )
  dim as Boolean sieve( limit )
  long i, j

  for i = 2 to limit
    sieve(i) = _true
  next

  for i = 2 to sqr( limit )
    if sieve(i) = _true
      j = i * i
      while j <= limit
        sieve(j) = _false
        j = j + i
      wend
    end if
  next

  for i = 2 to limit
    if sieve(i) = _true
      print i; " ";
    end if
  next
  print
end fn

fn SieveOfEratosthenes( 100 )

HandleEvents
