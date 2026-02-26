(* FreshML - Lambda Calculus with Native Binders *)
(* FreshML extends Standard ML with abstract names and binding types *)

(* Lambda calculus term type *)
datatype term =
    Var of name            (* variable reference *)
  | App of term * term     (* function application *)
  | Lam of <<name>> term   (* lambda abstraction with binder *)

(* Structural size of a term *)
fun size (Var _)        = 1
  | size (App(t1, t2))  = 1 + size t1 + size t2
  | size (Lam(<<_>> t)) = 1 + size t

(* Depth of the term tree *)
fun depth (Var _)        = 0
  | depth (App(t1, t2))  = 1 + Int.max(depth t1, depth t2)
  | depth (Lam(<<_>> t)) = 1 + depth t

(* Free variable check: is x free in t? *)
fun is_free (x : name) (Var y)         = (x = y)
  | is_free x            (App(t1, t2)) = is_free x t1 orelse is_free x t2
  | is_free x            (Lam(<<y>> t)) = is_free x t  (* y is fresh, so y <> x *)
