% Example PROGOL program for learning family relationships
% Mode declarations
:- modeh(1, parent(+person, +person))?
:- modeb(*, father(+person, -person))?
:- modeb(*, mother(+person, -person))?

% Background knowledge
father(tom, bob).
father(tom, liz).
mother(trude, bob).
mother(trude, liz).

% Positive examples
parent(tom, bob).
parent(tom, liz).
parent(trude, bob).
parent(trude, liz).

% Negative examples (optional)
% parent(bob, tom).
% parent(liz, trude).
