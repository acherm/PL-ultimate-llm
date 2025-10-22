type token = Plus | Minus | Times | Div | Num of int | Lparen | Rparen

let rec expr = parser
  | [< x = term; e = expr_cont >] -> e x
and expr_cont = parser
  | [< 'Plus; x = term; e = expr_cont >] -> (fun y -> e (x + y))
  | [< 'Minus; x = term; e = expr_cont >] -> (fun y -> e (x - y))
  | [< >] -> (fun x -> x)
and term = parser
  | [< x = fact; t = term_cont >] -> t x
and term_cont = parser
  | [< 'Times; x = fact; t = term_cont >] -> (fun y -> t (x * y))
  | [< 'Div; x = fact; t = term_cont >] -> (fun y -> t (x / y))
  | [< >] -> (fun x -> x)
and fact = parser
  | [< 'Num x >] -> x
  | [< 'Lparen; x = expr; 'Rparen >] -> x