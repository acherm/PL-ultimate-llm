-- Snowflake Scripting: Fibonacci sequence
-- Returns the nth Fibonacci number using iteration
CREATE OR REPLACE PROCEDURE fibonacci(n INTEGER)
  RETURNS INTEGER
  LANGUAGE SQL
AS
DECLARE
  a INTEGER DEFAULT 0;
  b INTEGER DEFAULT 1;
  temp INTEGER;
  i INTEGER DEFAULT 2;
BEGIN
  IF (n <= 0) THEN
    RETURN 0;
  ELSEIF (n = 1) THEN
    RETURN 1;
  END IF;
  WHILE (i <= n) DO
    temp := a + b;
    a := b;
    b := temp;
    i := i + 1;
  END WHILE;
  RETURN b;
END;
