; Fibonacci sequence in Cadence SKILL
procedure(fibonacci(n)
  if(n <= 1 then n
  else fibonacci(n-1) + fibonacci(n-2))
)

let((result)
  for(i 0 10
    result = fibonacci(i)
    printf("fibonacci(%d) = %d\n" i result)
  )
)
