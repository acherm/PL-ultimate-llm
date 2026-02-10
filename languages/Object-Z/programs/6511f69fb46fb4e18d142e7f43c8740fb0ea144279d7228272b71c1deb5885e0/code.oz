Counter
  value: ℕ

INIT
  value = 0

Increment
  Δ(value)
  value' = value + 1

Decrement
  Δ(value)
  value > 0
  value' = value - 1

GetValue
  ξ(value)
  result!: ℕ
  result! = value
