method BinarySearch(a: array<int>, key: int) returns (index: int)
  requires a != null && a.Length > 0
  requires forall i,j :: 0 <= i < j < a.Length ==> a[i] <= a[j]
  ensures -1 <= index < a.Length
  ensures index == -1 ==> forall k :: 0 <= k < a.Length ==> a[k] != key
  ensures 0 <= index ==> a[index] == key
{
  var low := 0;
  var high := a.Length;
  index := -1;
  while low < high && index == -1
    invariant 0 <= low <= high <= a.Length
    invariant index == -1 ==> forall k :: 0 <= k < low || high <= k < a.Length ==> a[k] != key
    invariant -1 <= index < a.Length
    invariant index != -1 ==> 0 <= index < a.Length && a[index] == key
  {
    var mid := (low + high) / 2;
    if a[mid] < key {
      low := mid + 1;
    } else if key < a[mid] {
      high := mid;
    } else {
      index := mid;
    }
  }
}