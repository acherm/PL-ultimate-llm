MODULE Hello EXPORTS Main;

IMPORT IO, Params, Text;

BEGIN
  IO.Put("Hello world!\n");
  FOR i := 1 TO Params.Count-1 DO
    IO.Put(Params.Get(i));
    IF i < Params.Count-1 THEN IO.Put(" ") END;
  END;
  IF Params.Count > 1 THEN IO.Put("\n") END;
END Hello.