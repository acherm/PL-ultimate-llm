module LabeledCrypto

open FStar.Mul

type label = L | H
let (<=) l1 l2 = (l1=L) \/ (l1=l2)

type labeled_int (l:label) = x:int

let label_of (x:int) : label = if x > 1000 then H else L

let lift (l:label) (x:int) : labeled_int l = x

let combine (l1:label) (l2:label) : Tot label = if l1=H \/ l2=H then H else L

let add (l1:label) (l2:label) (x:labeled_int l1) (y:labeled_int l2)
  : labeled_int (combine l1 l2)
  = x + y

let declassify (l:label) (x:labeled_int l) : Tot (labeled_int L) = x

let public_release (x:int) : labeled_int L = x

let x = lift L 10
let y = lift H 2000

let z = add L H x y

let z' : labeled_int H = z

let z'' = declassify H z

let z''' : labeled_int L = z''
