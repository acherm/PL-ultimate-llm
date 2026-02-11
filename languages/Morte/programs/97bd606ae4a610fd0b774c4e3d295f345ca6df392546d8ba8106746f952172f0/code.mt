(   \(n : *)
->  \(f : n -> n)
->  \(x : n)
->  (   \(list : *)
    ->  \(cons : * -> list -> list)
    ->  \(nil : list)
    ->  n
    ) n (\(_ : *) -> \(y : n) -> f y) x
) (* -> *) (\(a : *) -> a) (\(a : *) -> a)
