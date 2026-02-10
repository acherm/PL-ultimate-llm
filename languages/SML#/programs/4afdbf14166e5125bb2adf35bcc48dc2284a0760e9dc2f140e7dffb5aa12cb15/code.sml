fun quicksort [] = []
  | quicksort (pivot::rest) =
      let
        val (less, greater) = List.partition (fn x => x < pivot) rest
      in
        quicksort less @ [pivot] @ quicksort greater
      end

val test = quicksort [3, 7, 1, 9, 2, 5, 8, 4, 6]
val () = print (String.concatWith " " (map Int.toString test) ^ "\n")
