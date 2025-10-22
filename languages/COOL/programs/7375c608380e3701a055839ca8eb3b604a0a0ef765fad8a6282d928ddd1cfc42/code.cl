class Main inherits IO {
  main(): SELF_TYPE {
    out_string("Factorial of 5 is: ").out_int(factorial(5)).out_string("\n")
  };

  factorial(n: Int): Int {
    if n <= 1 then 1 else n * factorial(n - 1) fi
  };
};