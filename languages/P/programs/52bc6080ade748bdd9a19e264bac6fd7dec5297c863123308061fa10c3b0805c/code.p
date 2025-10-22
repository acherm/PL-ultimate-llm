module Example1

// Define an event
event e1(x: int) =
  { print(0, "e1 triggered with x = ", x); }

// Define a machine
machine M
  { // Define the initial state
  state S0 =
    { // Define the initial action
      on e1(x) =>
        { print(0, "S0 received e1 with x = ", x); }
      // Define the initial invariant
      invariant x >= 0;
    }
  }

// Define the main
main
  {
    // Create an instance of machine M
    instance m: M;
    // Trigger event e1
    trigger e1(10);
  }
