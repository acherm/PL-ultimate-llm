mode producer(out).
producer([H|T]) :-
    produce(H),
    producer(T).
producer([]).

mode consumer(in).
consumer([H|T]) :-
    consume(H),
    consumer(T).
consumer([]).

mode produce(out).
produce(1).
produce(2).
produce(3).

mode consume(in).
consume(X) :-
    write(X), nl.

mode main.
main :-
    producer(L) & consumer(L).