factorial = method(n,
  if(n <= 1,
    1,
    n * factorial(n - 1)
  )
)

; Test the factorial function
5 times(i,
  "factorial(#{i}) = #{factorial(i)}" println
)
