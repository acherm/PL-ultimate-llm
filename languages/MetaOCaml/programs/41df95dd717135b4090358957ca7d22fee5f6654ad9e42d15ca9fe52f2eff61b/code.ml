(* Staged power function *)
let rec power n x =
  if n = 0 then .<1>.
  else if n mod 2 = 0 then
    let y = power (n/2) x in
    .<.~y * .~y>.
  else
    let y = power (n-1) x in
    .<x * .~y>.

(* Generate specialized power function *)
let power3 = .<fun x -> .~(power 3 .<x>.)>.

(* Compile and run *)
let () =
  let f = Runcode.run power3 in
  Printf.printf "3^3 = %d\n" (f 3)
