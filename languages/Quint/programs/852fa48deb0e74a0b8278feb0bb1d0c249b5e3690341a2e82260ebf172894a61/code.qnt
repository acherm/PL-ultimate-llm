// A simple counter specification
module counter {
  var count: int
  
  pure val MAX = 10
  
  action init = {
    count' = 0
  }
  
  action increment = {
    require(count < MAX),
    count' = count + 1
  }
  
  action decrement = {
    require(count > 0),
    count' = count - 1
  }
  
  action step = {
    any {
      increment,
      decrement,
    }
  }
  
  val neverNegative = count >= 0
  val neverExceedsMax = count <= MAX
}
