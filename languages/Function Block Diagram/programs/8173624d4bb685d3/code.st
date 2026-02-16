(* Simple Function Block Diagram Program *)
(* AND gate with two inputs leading to output *)

PROGRAM AND_Gate
VAR
    Input1 : BOOL;
    Input2 : BOOL;
    Output : BOOL;
END_VAR

(* Function Block: AND *)
Output := Input1 AND Input2;

END_PROGRAM
