CREATE FUNCTION dbo.SplitStrings_CTE
(
   @List       NVARCHAR(MAX),
   @Delimiter  NVARCHAR(255)
)
RETURNS TABLE
WITH SCHEMABINDING
AS
   RETURN
   (
      WITH n(n) AS
      (
        SELECT 1 UNION ALL SELECT n+1
        FROM n WHERE n < 4000
      )
      SELECT
        Item = SUBSTRING(@List, n, CHARINDEX(@Delimiter, @List + @Delimiter, n) - n)
      FROM
      (
        SELECT n = 1
        UNION ALL
        SELECT n + 1
        FROM n
        WHERE n < LEN(@List) AND SUBSTRING(@List, n, 1) = @Delimiter
      ) AS a
      OPTION (MAXRECURSION 0)
   );
GO