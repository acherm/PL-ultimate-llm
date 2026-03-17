-- pgScript: Fibonacci sequence using script-level variables
DECLARE @a INT;
DECLARE @b INT;
DECLARE @temp INT;
DECLARE @count INT;
DECLARE @limit INT;

SET @limit = 10;
SET @a = 0;
SET @b = 1;
SET @count = 0;

PRINT 'Fibonacci sequence:';
WHILE @count < @limit
BEGIN
    PRINT @a;
    SET @temp = @a + @b;
    SET @a = @b;
    SET @b = @temp;
    SET @count = @count + 1;
END
