function fast_fib_module(stdlib, foreign, heap) {
  "use asm";
  function fib(n) {
    n = n|0;
    if (n >>> 0 < 3) {
      return 1|0;
    }
    return (fib((n-1)|0) + fib((n-2)|0))|0;
  }
  return fib;
}

fast_fib = fast_fib_module(window);

function slow_fib(n) {
  if (n < 3) {
    return 1;
  }
  return slow_fib(n-1) + slow_fib(n-2);
}
