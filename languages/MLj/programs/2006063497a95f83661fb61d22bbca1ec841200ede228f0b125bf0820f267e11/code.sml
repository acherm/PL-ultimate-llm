(* Quicksort in MLj/Standard ML *)
fun quicksort [] = []
  | quicksort (x::xs) =
    let
      val smaller = List.filter (fn y => y < x) xs
      val greater = List.filter (fn y => y >= x) xs
    in
      quicksort smaller @ [x] @ quicksort greater
    end

val () =
  let
    val lst = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    val sorted = quicksort lst
    fun printList [] = print "\n"
      | printList (x::xs) = (print (Int.toString x ^ " "); printList xs)
  in
    print "Sorted: ";
    printList sorted
  end
