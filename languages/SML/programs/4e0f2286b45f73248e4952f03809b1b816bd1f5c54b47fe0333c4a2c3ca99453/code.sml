fun quicksort [] = []
  | quicksort (x::xs) =
    let
      val smaller = List.filter (fn y => y < x) xs
      val greater = List.filter (fn y => y >= x) xs
    in
      quicksort smaller @ [x] @ quicksort greater
    end

val result = quicksort [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
val () = List.app (fn x => print (Int.toString x ^ " ")) result
val () = print "\n"
