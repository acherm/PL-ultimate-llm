let fib n =
  let rec fib_aux n a b =
    if n = 0 then a
    else fib_aux (n - 1) b (a + b)
  in
  fib_aux n 0 1
