----------------------------- MODULE DieHard -----------------------------
EXTENDS Integers

(*
--algorithm DieHard
variables big = 5, small = 0 ;
begin
  while big # 4 do
    either
      big := 8 ;
    or
      small := 0 ;
    or
      small := 3 ;
    or
      with transfer = min(big, 3 - small) do
        big := big - transfer ;
        small := small + transfer ;
      end with;
    or
      with transfer = min(small, 8 - big) do
        small := small - transfer ;
        big := big + transfer ;
      end with;
    end either;
  end while;
  assert big = 4;
end algorithm;
*)

\* This is the translation of the PlusCal algorithm.
\* You can see it by going to the "File" menu and choosing
\* "Translate PlusCal Algorithm".  However, you will see that
\* the translation of the "with" statement is rather complicated.
\* This is because the translator has to handle the general case.
\* It is much simpler to write the TLA+ spec directly.  Here is
\* a simpler version of the spec.

VARIABLES big, small

JugCapacity == 3..8 \* A hack to make TLC run faster.

TypeOK == /\ big \in 0..8
           /\ small \in 0..3

Init == /\ big = 0
        /\ small = 0

FillBig == /\ big' = 8
           /\ small' = small

FillSmall == /\ small' = 3
             /\ big' = big

EmptyBig == /\ big' = 0
            /\ small' = small

EmptySmall == /\ small' = 0
              /\ big' = big

SmallToBig == /\ LET transfer == min(small, 8 - big)
               IN  /\ big' = big + transfer
                   /\ small' = small - transfer

BigToSmall == /\ LET transfer == min(big, 3 - small)
               IN  /\ big' = big - transfer
                   /\ small' = small + transfer

Next == \/ FillBig
        \/ FillSmall
        \/ EmptyBig
        \/ EmptySmall
        \/ SmallToBig
        \/ BigToSmall

Spec == Init /\ [][Next]_<<big, small>>

FourGallonsInBig == big = 4

=============================================================================