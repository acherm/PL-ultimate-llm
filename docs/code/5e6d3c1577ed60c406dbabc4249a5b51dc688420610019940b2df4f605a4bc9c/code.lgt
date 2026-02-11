:- object(hello).

:- public(greet/0).

greet :-
    write('Hello, World!'), nl.

:- end_object.