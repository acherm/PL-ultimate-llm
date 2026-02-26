:- use_module(library(aleph)).
:- if(current_predicate(use_rendering/1)).
:- use_rendering(prolog).
:- endif.
:- aleph.

:- set(i,2).
:- set(clauselength,4).

:- modeh(1,class(+animal,-class)).
:- modeb(1,has_legs(+animal,#int)).
:- modeb(1,has_tail(+animal)).
:- modeb(1,has_gills(+animal)).
:- modeb(1,has_feathers(+animal)).
:- modeb(1,isa(+animal,#type)).

has_legs(dog,4).
has_legs(cat,4).
has_legs(trout,0).
has_legs(herring,0).
has_legs(shark,0).
has_legs(eel,0).
has_legs(cobra,0).
has_legs(rattlesnake,0).
has_legs(boa,0).
has_legs(tortoise,4).
has_legs(eagle,2).
has_legs(albatross,2).

has_tail(dog).
has_tail(cat).
has_tail(trout).
has_tail(herring).
has_tail(shark).
has_tail(eel).
has_tail(cobra).
has_tail(rattlesnake).
has_tail(boa).
has_tail(tortoise).
has_tail(eagle).
has_tail(albatross).

has_gills(trout).
has_gills(herring).
has_gills(shark).
has_gills(eel).

has_feathers(eagle).
has_feathers(albatross).

isa(dog,mammal).
isa(cat,mammal).
isa(trout,fish).
isa(herring,fish).
isa(shark,fish).
isa(eel,fish).
isa(cobra,reptile).
isa(rattlesnake,reptile).
isa(boa,reptile).
isa(tortoise,reptile).
isa(eagle,bird).
isa(albatross,bird).

:- begin_in_pos.
class(dog,mammal).
class(cat,mammal).
class(trout,fish).
class(herring,fish).
class(shark,fish).
class(eel,fish).
class(cobra,reptile).
class(rattlesnake,reptile).
class(boa,reptile).
class(tortoise,reptile).
class(eagle,bird).
class(albatross,bird).
:- end_in_pos.

:- induce.
