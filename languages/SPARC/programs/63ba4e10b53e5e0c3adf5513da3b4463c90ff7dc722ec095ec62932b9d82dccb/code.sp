sorts
  #node = {a, b, c, d, e}.
  #color = {red, blue, green}.

predicates
  edge(#node, #node).
  colored(#node, #color).

rules
  edge(a, b). edge(b, c). edge(c, d). edge(d, e). edge(e, a). edge(a, c).

  1{colored(X, C) : #color(C)}1 :- #node(X).

  :- edge(X, Y), colored(X, C), colored(Y, C).
