#!/usr/local/bin/siod -v01,-m2
#-*-mode:text;parser:pratt-*-

main() :=
{writes(nil,"Hello Scheme World.\n");
 fflush(nil);
 writes(nil,"fib(20) = ",fib(20),"\n");
}
$

fib(x) := if x < 2 then x else fib(x-1) + fib(x-2)
$
