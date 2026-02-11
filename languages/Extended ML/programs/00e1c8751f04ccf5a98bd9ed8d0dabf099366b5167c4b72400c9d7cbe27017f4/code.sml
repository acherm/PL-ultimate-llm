signature STACK =
sig
  type 'a stack
  exception Empty
  val empty : 'a stack
  val push : 'a * 'a stack -> 'a stack
  val pop : 'a stack -> 'a * 'a stack
  val top : 'a stack -> 'a
  axiom empty_push : forall x:'a. top(push(x, empty)) = x
  axiom push_pop : forall x:'a, s:'a stack. pop(push(x, s)) = (x, s)
end
