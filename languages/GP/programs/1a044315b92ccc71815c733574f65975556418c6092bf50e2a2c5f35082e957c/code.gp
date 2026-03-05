fibonacci(n) = {
  if (n <= 1, return(n));
  my(a = 0, b = 1, t);
  for(i = 2, n,
    t = a + b;
    a = b;
    b = t;
  );
  b
}

for(n = 0, 10, print(fibonacci(n)))
