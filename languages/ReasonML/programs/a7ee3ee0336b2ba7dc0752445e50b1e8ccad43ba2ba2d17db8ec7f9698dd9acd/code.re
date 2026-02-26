let rec fib = (n) =>
  switch (n) {
  | 0 => 0
  | 1 => 1
  | n => fib(n - 1) + fib(n - 2)
  };

let () =
  for (i in 0 to 10) {
    Printf.printf("fib(%d) = %d\n", i, fib(i))
  };
