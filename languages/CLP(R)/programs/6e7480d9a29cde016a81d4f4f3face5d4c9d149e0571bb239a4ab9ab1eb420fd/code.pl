% Pythagorean triple solver using CLP(R)
% Finds integer solutions to a^2 + b^2 = c^2

pythagorean(A, B, C) :-
    A >= 1,
    B >= A,
    C >= B,
    A * A + B * B = C * C,
    A =< 20,
    B =< 20,
    C =< 25.

% Query example:
% ?- pythagorean(A, B, C).
% A = 3, B = 4, C = 5
% A = 5, B = 12, C = 13
% A = 8, B = 15, C = 17

% Rectangle area and perimeter constraint example
rectangle(Width, Height, Area, Perimeter) :-
    Width > 0,
    Height > 0,
    Area = Width * Height,
    Perimeter = 2 * (Width + Height).
