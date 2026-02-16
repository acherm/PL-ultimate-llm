type nat = rec t. unit + t ;;

let zero = inl () ;;
let succ = fun n -> inr n ;;

let rec add = fun m n ->
  case m of
    inl _ -> n
  | inr m' -> succ (add m' n)
  end
;;

let one = succ zero ;;
let two = succ one ;;
let three = add one two ;;
