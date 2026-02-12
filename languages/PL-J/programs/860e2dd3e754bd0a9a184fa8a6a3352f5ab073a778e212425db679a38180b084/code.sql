CREATE FUNCTION javaToUpper(VARCHAR(80))
  RETURNS VARCHAR(80)
  AS 'UDR:org.postgresql.pljava.example.StringFunctions.toUpperCase'
  LANGUAGE java;

CREATE FUNCTION javaConcat(VARCHAR(80), VARCHAR(80))
  RETURNS VARCHAR(80)
  AS 'UDR:org.postgresql.pljava.example.StringFunctions.concat'
  LANGUAGE java;

SELECT javaToUpper('hello world');
SELECT javaConcat('Hello ', 'World');
