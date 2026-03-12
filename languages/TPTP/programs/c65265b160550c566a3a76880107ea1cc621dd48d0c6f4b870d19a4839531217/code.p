%--------------------------------------------------------------------------
% File     : SYL001+1 : TPTP v8.1.0. Released v2.0.0.
% Domain   : Syllogisms (Barbara - 1)
% Problem  : Barbara
% Version  : Especial.
% English  : Barbara: All X are Y; All Y are Z; All X are Z.
%--------------------------------------------------------------------------

fof(barbara_syllogism,conjecture,
    ( ! [A,B,C] :
        ( ( ! [X] : (A(X) => B(X))
          & ! [X] : (B(X) => C(X)))
       => ! [X] : (A(X) => C(X))))).

%--------------------------------------------------------------------------