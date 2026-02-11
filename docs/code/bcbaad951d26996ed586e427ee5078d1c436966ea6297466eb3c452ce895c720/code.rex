/* REXX program to calculate the Ackermann function. */
/* This version uses a stack to avoid recursion limits. */

parse arg m n .
if m = '' | n = '' then do
  say "Usage: ack m n"
  say "where m and n are non-negative integers."
  exit
end

if \datatype(m, 'W') | \datatype(n, 'W') then do
  say "Error: m and n must be non-negative integers."
  exit
end

stack = .list~new
stack~push(m)

do while stack~size > 0
  m = stack~pop
  if m = 0 then
    n = n + 1
  else if n = 0 then do
    n = 1
    stack~push(m - 1)
  end
  else do
    stack~push(m - 1)
    stack~push(m)
    n = n - 1
  end
end

say n
exit

::class 'list' public
::method init
  expose items
  items = .array~new

::method push
  expose items
  use arg item
  items~append(item)

::method pop
  expose items
  if items~items = 0 then
    return .nil
  item = items[items~items]
  items~remove(items~items)
  return item

::method size
  expose items
  return items~items