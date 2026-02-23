counter(In) :-
    counter(In,0).

counter(In,_) :-
  In =?= [clear|In'] |
    counter(In',0).
counter(In,C) :-
  In =?= [increment|In'] |
    C' := C + 1,
    counter(In',C').
counter(In,C) :-
  In =?= [read(V)|In'] |
    V = C,
    counter(In',C).
counter(In,_) :-
  In =?= [] | true.
