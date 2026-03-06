PROGRAM MotorControl
VAR
  START  : BOOL;  (* Normally open push button *)
  STOP_N : BOOL;  (* Normally closed stop button *)
  MOTOR  : BOOL;  (* Motor output coil *)
  LAMP   : BOOL;  (* Indicator lamp *)
END_VAR

(* Rung 1: Motor Start/Stop circuit with seal-in (latching) contact *)
(*                                                                   *)
(*  |----[ START ]----+----[/STOP_N]----( MOTOR )----|              *)
(*                    |                               |              *)
(*  |----[ MOTOR ]----+                               |              *)
(*                                                                   *)
(* The MOTOR contact in parallel with START creates a holding circuit *)
(* Once MOTOR energizes, it seals itself in until STOP_N opens.      *)

LD   START
OR   MOTOR
ANDN STOP_N
ST   MOTOR

(* Rung 2: Indicator lamp follows motor state *)
(*                                            *)
(*  |----[ MOTOR ]----( LAMP )----|           *)

LD   MOTOR
ST   LAMP

END_PROGRAM
