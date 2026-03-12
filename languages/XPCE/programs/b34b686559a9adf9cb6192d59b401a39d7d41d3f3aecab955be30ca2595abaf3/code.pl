:- use_module(library(pce)).

hello_world :-
    new(D, dialog('Hello World')),
    send(D, append, label(text, 'Hello, World!')),
    send(D, open).

:- initialization(hello_world, main).
