spec Stack is
  type Stack(a)
  op empty   : [a] Stack(a)
  op push    : [a] a * Stack(a) -> Stack(a)
  op pop     : [a] Stack(a) -> Stack(a)
  op top     : [a] Stack(a) -> a
  op isEmpty : [a] Stack(a) -> Bool

  axiom isEmpty_empty is [a]
    isEmpty(empty) = true

  axiom isEmpty_push is [a]
    fa(x : a, s : Stack(a))
      isEmpty(push(x, s)) = false

  axiom top_push is [a]
    fa(x : a, s : Stack(a))
      top(push(x, s)) = x

  axiom pop_push is [a]
    fa(x : a, s : Stack(a))
      pop(push(x, s)) = s
end-spec
