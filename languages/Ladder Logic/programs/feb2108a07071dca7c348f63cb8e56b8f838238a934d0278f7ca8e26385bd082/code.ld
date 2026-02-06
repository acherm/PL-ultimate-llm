(* Simple Traffic Light Controller in Ladder Logic *)
(* Uses timers to cycle through Red, Yellow, Green *)

PROGRAM TrafficLight
VAR
    Red_Light : BOOL;
    Yellow_Light : BOOL;
    Green_Light : BOOL;
    Timer_Red : TON;
    Timer_Yellow : TON;
    Timer_Green : TON;
    Cycle_Start : BOOL := TRUE;
END_VAR

(* Red Light Logic *)
Timer_Red(IN := Cycle_Start OR Timer_Yellow.Q, PT := T#30s);
Red_Light := Timer_Red.Q;

(* Yellow Light Logic *)
Timer_Yellow(IN := Timer_Green.Q, PT := T#5s);
Yellow_Light := Timer_Yellow.Q;

(* Green Light Logic *)
Timer_Green(IN := Timer_Red.Q, PT := T#25s);
Green_Light := Timer_Green.Q;

(* Reset cycle *)
IF Timer_Yellow.Q THEN
    Cycle_Start := TRUE;
END_IF;

END_PROGRAM
