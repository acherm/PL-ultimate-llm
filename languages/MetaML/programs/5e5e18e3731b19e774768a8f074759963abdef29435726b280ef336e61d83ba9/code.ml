(* MetaML: Staged Power Function *)
(* from Taha, W. "A Gentle Introduction to Multi-stage Programming" *)

let rec power : int -> <int -> int> =
  fun n ->
    if n = 0 then
      <fun _ -> 1>
    else
      <fun x -> x * ~(power (n-1)) x>

let () =
  let p3 = run (power 3) in
  Printf.printf "2^3 = %d\n" (p3 2);
  Printf.printf "3^3 = %d\n" (p3 3);
  Printf.printf "4^3 = %d\n" (p3 4)
