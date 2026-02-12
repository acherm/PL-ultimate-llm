(* Quicksort implementation in Standard ML *)
fun quicksort [] = []
  | quicksort (pivot::rest) =
    let
      val (less, greater) = List.partition (fn x => x < pivot) rest
    in
      quicksort less @ [pivot] @ quicksort greater
    end;

(* Test the quicksort function *)
val test_list = [3, 7, 1, 9, 2, 8, 4, 6, 5];
val sorted = quicksort test_list;

print "Original list: ";
print (String.concatWith ", " (map Int.toString test_list));
print "\n";
print "Sorted list: ";
print (String.concatWith ", " (map Int.toString sorted));
print "\n";