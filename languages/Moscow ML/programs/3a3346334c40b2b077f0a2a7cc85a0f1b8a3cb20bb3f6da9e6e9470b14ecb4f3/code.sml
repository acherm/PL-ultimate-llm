(* Quicksort implementation in Moscow ML *)

fun quicksort [] = []
  | quicksort (pivot::rest) =
    let
      val (less, greater) = List.partition (fn x => x < pivot) rest
    in
      quicksort less @ [pivot] @ quicksort greater
    end;

(* Example usage *)
val test_list = [3, 7, 1, 9, 2, 5, 8, 4, 6];
val sorted = quicksort test_list;
