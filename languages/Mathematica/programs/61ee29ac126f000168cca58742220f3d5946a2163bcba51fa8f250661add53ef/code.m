(* Compute first 20 Fibonacci numbers *)
Fibonacci[n_] := Fibonacci[n] = If[n < 2, n, Fibonacci[n-1] + Fibonacci[n-2]]

(* Generate list *)
fibList = Table[Fibonacci[i], {i, 0, 19}]

(* Display results *)
Print["First 20 Fibonacci numbers:"]
Print[fibList]

(* Find sum of even Fibonacci numbers *)
evenSum = Total[Select[fibList, EvenQ]]
Print["Sum of even Fibonacci numbers: ", evenSum]
