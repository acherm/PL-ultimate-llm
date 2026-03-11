(* Galileo program: basic geometric operations *)

is type Point = {x: real, y: real};

is fun square : real -> real =
  fun n => n * n;

is fun distance : Point -> Point -> real =
  fun p q =>
    let dx = p.x - q.x in
    let dy = p.y - q.y in
    sqrt (square dx + square dy);

is val origin : Point = {x = 0.0, y = 0.0};

is val p : Point = {x = 3.0, y = 4.0};

is val result : real = distance origin p;
