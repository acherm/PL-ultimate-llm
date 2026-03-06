% N-Queens problem in ASP (Gringo/Clingo)
#const n = 8.

% Guess placement: exactly one queen per row
1 { queen(I,1..n) } 1 :- I = 1..n.

% No two queens in the same column
:- queen(I,J), queen(K,J), I != K.

% No two queens on the same diagonal
:- queen(I,J), queen(K,L), I != K, |I-K| = |J-L|.

#show queen/2.
