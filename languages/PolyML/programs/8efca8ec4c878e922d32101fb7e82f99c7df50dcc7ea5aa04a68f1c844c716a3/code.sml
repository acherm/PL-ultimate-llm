fun quicksort [] = []
  | quicksort (pivot::rest) =
      let
        val (smaller, larger) = List.partition (fn x => x < pivot) rest
      in
        quicksort smaller @ [pivot] @ quicksort larger
      end;

val numbers = [64, 34, 25, 12, 22, 11, 90];
val sorted = quicksort numbers;

print "Original: ";
app (fn x => print (Int.toString x ^ " ")) numbers;
print "\nSorted: ";
app (fn x => print (Int.toString x ^ " ")) sorted;
print "\n";
