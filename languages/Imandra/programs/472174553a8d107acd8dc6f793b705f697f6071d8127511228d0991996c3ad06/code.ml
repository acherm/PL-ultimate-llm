(* Simple list reversal function in Imandra *)
let rec rev l =
  match l with
  | [] -> []
  | x :: xs -> rev xs @ [x]

(* Property to verify: reversing twice gives original list *)
let rev_involutive l = rev (rev l) = l

(* Verify the property *)
verify rev_involutive
