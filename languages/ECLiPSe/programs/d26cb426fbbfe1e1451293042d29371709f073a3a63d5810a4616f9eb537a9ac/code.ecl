:- lib(ic).

queens(N, Board) :-
    length(Board, N),
    Board :: 1..N,
    ( for(I,1,N), param(Board) do
        ( for(J,I+1,N), param(Board,I) do
            Board[I] #\= Board[J],
            Board[I] - Board[J] #\= I - J,
            Board[I] - Board[J] #\= J - I
        )
    ),
    labeling(Board).

solve_queens(N) :-
    queens(N, Board),
    writeln(Board).
