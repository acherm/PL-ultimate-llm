open Hardcaml
open Signal

module Full_adder = struct
  type 'a t =
    { a : 'a
    ; b : 'a
    ; carry_in : 'a
    } [@@deriving sexp_of, hardcaml]

  module O = struct
    type 'a t =
      { sum : 'a
      ; carry_out : 'a
      } [@@deriving sexp_of, hardcaml]
  end

  let create (i : _ t) =
    let sum1 = i.a ^: i.b in
    let carry1 = i.a &: i.b in
    let sum = sum1 ^: i.carry_in in
    let carry2 = sum1 &: i.carry_in in
    let carry_out = carry1 |: carry2 in
    { O.sum; carry_out }
end

let () =
  let module Circuit = Hardcaml.Circuit.With_interface (Full_adder) (Full_adder.O) in
  let circuit = Circuit.create_exn ~name:"full_adder" Full_adder.create in
  Rtl.print Verilog circuit