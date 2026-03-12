CREATE PROCEDURE UPDATE_SALARY_IF (IN empNum CHAR(6), IN rating SMALLINT)
  LANGUAGE SQL
  BEGIN
    IF (rating = 1) THEN
      UPDATE employee
        SET salary = salary * 1.10, bonus = 1000
        WHERE empno = empNum;
    ELSEIF (rating = 2) THEN
      UPDATE employee
        SET salary = salary * 1.05, bonus = 500
        WHERE empno = empNum;
    ELSE
      UPDATE employee
        SET salary = salary * 1.03, bonus = 0
        WHERE empno = empNum;
    END IF;
  END