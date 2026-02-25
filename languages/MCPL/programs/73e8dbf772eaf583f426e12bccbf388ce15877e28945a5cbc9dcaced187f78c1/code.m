GET "libhdr"

FUN fib : 0 => 0
        | 1 => 1
        | n => fib(n-1) + fib(n-2)

AND start : _ =>
{ LET i = 0
  WHILE i <= 10 DO
  { writef("fib(%i2) = %i3*n", i, fib i)
    i := i + 1
  }
}
