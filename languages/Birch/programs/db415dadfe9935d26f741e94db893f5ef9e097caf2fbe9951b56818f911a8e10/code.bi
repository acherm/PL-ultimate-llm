program hello() {
  /* Simple Birch program demonstrating basic syntax */
  let x:Real <- 0.0;
  x <- simulate_gaussian(0.0, 1.0);

  if x > 0.0 {
    write("Positive value: " + x + "\n");
  } else {
    write("Non-positive value: " + x + "\n");
  }

  /* Demonstrate array usage */
  let values:Real[10];
  for i in 1..10 {
    values[i] <- simulate_gaussian(0.0, 1.0);
  }

  write("Generated " + length(values) + " random values\n");
}
