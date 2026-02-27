sieve[n_] := Module[{s = Table[True, {n}]},
  s[[1]] = False;
  Do[If[s[[i]], Do[s[[j]] = False, {j, i^2, n, i}]], {i, 2, Sqrt[n]}];
  Flatten[Position[s, True]]
]
