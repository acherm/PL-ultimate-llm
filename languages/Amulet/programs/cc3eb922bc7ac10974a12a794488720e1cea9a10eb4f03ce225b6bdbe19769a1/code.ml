(* Quicksort implementation in Amulet *)
let rec quicksort = function
  | [] -> []
  | x :: xs ->
      let smaller = List.filter (fun y -> y < x) xs
      let larger = List.filter (fun y -> y >= x) xs
      quicksort smaller @ [x] @ quicksort larger

let () =
  let test_list = [3; 1; 4; 1; 5; 9; 2; 6; 5; 3; 5]
  let sorted = quicksort test_list
  print_endline (show sorted)
