datatype 'a tree = Empty | Node of 'a tree * 'a * 'a tree

fun insert (x, Empty) = Node(Empty, x, Empty)
  | insert (x, Node(left, y, right)) =
      if x < y
      then Node(insert(x, left), y, right)
      else if x > y
      then Node(left, y, insert(x, right))
      else Node(left, x, right)

fun member (x, Empty) = false
  | member (x, Node(left, y, right)) =
      if x < y
      then member(x, left)
      else if x > y
      then member(x, right)
      else true

fun fromList xs = foldr insert Empty xs