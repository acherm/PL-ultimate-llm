MODULE GCDDemo;
(* Demonstrates GCD and LCM in Modula-2+ *)
FROM InOut IMPORT WriteInt, WriteLn, WriteString;

PROCEDURE GCD(a, b: INTEGER): INTEGER;
VAR t: INTEGER;
BEGIN
  WHILE b # 0 DO
    t := b;
    b := a MOD b;
    a := t
  END;
  RETURN a
END GCD;

PROCEDURE LCM(a, b: INTEGER): INTEGER;
BEGIN
  RETURN (a * b) DIV GCD(a, b)
END LCM;

BEGIN
  WriteString("GCD(48, 18) = "); WriteInt(GCD(48, 18), 0); WriteLn;
  WriteString("GCD(100, 75) = "); WriteInt(GCD(100, 75), 0); WriteLn;
  WriteString("LCM(4, 6) = "); WriteInt(LCM(4, 6), 0); WriteLn
END GCDDemo.
