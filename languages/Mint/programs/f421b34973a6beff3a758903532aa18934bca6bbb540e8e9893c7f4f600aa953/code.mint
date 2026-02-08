component Counter {
  state counter : Number = 0

  fun increment : Promise(Void) {
    next { counter: counter + 1 }
  }

  fun decrement : Promise(Void) {
    next { counter: counter - 1 }
  }

  fun render : Html {
    <div>
      <button onClick={decrement}>
        "Decrement"
      </button>

      <span>
        Number.toString(counter)
      </span>

      <button onClick={increment}>
        "Increment"
      </button>
    </div>
  }
}
