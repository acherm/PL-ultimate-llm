MODULE Sort.

IMPORT Lists.

PREDICATE   Sort : List(Integer) * List(Integer).
DELAY       Sort(l,s) UNTIL Ground(l).

Sort([],[]).
Sort([x|l],s) <-
        Partition(l,x,l1,l2) &
        Sort(l1,s1) &
        Sort(l2,s2) &
        Append(s1,[x|s2],s).

PREDICATE   Partition : List(Integer) * Integer * List(Integer) * List(Integer).
DELAY       Partition(l,p,s,b) UNTIL Ground(l) & Ground(p).

Partition([],p,[],[]).
Partition([x|l],p,[x|s],b) <-
        x =< p &
        Partition(l,p,s,b).
Partition([x|l],p,s,[x|b]) <-
        x > p &
        Partition(l,p,s,b).