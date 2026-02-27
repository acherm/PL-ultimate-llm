[<ReflectedDefinition>]
module Fibonacci

open FunScript
open FunScript.TypeScript

let rec fib n =
    match n with
    | 0 | 1 -> n
    | n     -> fib (n - 1) + fib (n - 2)

let main () =
    for i in 0 .. 10 do
        Globals.console.log(sprintf "fib(%d) = %d" i (fib i))

do main ()
