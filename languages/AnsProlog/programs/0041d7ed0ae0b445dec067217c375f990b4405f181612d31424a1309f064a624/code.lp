% 3-Graph Coloring in AnsProlog
% Based on the classic AnsProlog encoding by Gelfond and Leone

node(a). node(b). node(c). node(d). node(e).
edge(a,b). edge(b,c). edge(c,d). edge(d,e). edge(e,a). edge(a,c).

color(red). color(green). color(blue).

1 { assign(N,C) : color(C) } 1 :- node(N).

:- edge(N1,N2), assign(N1,C), assign(N2,C).

#show assign/2.