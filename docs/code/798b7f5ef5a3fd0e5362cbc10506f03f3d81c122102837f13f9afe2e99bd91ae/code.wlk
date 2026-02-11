object counter {
  var count = 0

  method increment() {
    count = count + 1
  }

  method decrement() {
    count = count - 1
  }

  method value() {
    return count
  }

  method reset() {
    count = 0
  }
}

program myProgram {
  counter.increment()
  counter.increment()
  counter.increment()
  console.println("Counter value: " + counter.value())
  counter.decrement()
  console.println("After decrement: " + counter.value())
  counter.reset()
  console.println("After reset: " + counter.value())
}
