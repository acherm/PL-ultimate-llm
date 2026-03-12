:- class animal.

:- iv name/1.
:- iv sound/1.

new(Name, Sound) :-
    name := Name,
    sound := Sound.

speak :-
    name(N), sound(S),
    format('~w says ~w!~n', [N, S]).

:- end_class animal.

:- class dog inherits animal.

new(Name) :- super::new(Name, woof).

fetch(Item) :-
    name(N),
    format('~w fetches the ~w~n', [N, Item]).

:- end_class dog.

:- class cat inherits animal.

new(Name) :- super::new(Name, meow).

purr :-
    name(N),
    format('~w purrs...~n', [N]).

:- end_class cat.

:- create(dog, D),
   D::new(rex),
   D::speak,
   D::fetch(ball),
   create(cat, C),
   C::new(whiskers),
   C::speak,
   C::purr.
