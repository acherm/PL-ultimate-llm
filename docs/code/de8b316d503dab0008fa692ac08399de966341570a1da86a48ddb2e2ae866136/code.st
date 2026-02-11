(* This is a simple program that controls a motor with a start/stop
   pushbutton station, and an overload protection. Additionally, the
   motor can only be started if a second condition is met (interlock).
   This is a very common industrial application. *)

PROGRAM motor_control
  VAR
    start_pb AT %IX0.0 : BOOL;
    stop_pb AT %IX0.1 : BOOL;
    overload AT %IX0.2 : BOOL;
    interlock AT %IX0.3 : BOOL;
    motor AT %QX0.0 : BOOL;
  END_VAR

  motor := (motor OR start_pb) AND NOT stop_pb AND NOT overload AND interlock;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms, PRIORITY := 0);
    PROGRAM instance0 OF motor_control WITH task0 : task0;
  END_RESOURCE
  
END_CONFIGURATION