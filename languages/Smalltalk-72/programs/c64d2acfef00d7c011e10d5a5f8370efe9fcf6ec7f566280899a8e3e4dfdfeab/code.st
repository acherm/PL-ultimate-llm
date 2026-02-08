to factorial n (
  n = 1 ifso: (↑ 1)
  n = 0 ifso: (↑ 1)
  ↑ n * factorial (n - 1)
)

factorial 5