(* Acute: Mergesort implementation *)
let rec merge xs ys =
  match xs, ys with
  | [], ys -> ys
  | xs, [] -> xs
  | x :: xs', y :: ys' ->
    if x <= y then x :: merge xs' ys
    else y :: merge xs ys'

let rec split = function
  | [] -> ([], [])
  | [x] -> ([x], [])
  | x :: y :: rest ->
    let (xs, ys) = split rest in
    (x :: xs, y :: ys)

let rec mergesort = function
  | [] -> []
  | [x] -> [x]
  | xs ->
    let (left, right) = split xs in
    merge (mergesort left) (mergesort right)

let () =
  let lst = [5; 3; 8; 1; 9; 2; 7; 4; 6] in
  let sorted = mergesort lst in
  List.iter (fun x -> Printf.printf "%d " x) sorted;
  print_newline ()
