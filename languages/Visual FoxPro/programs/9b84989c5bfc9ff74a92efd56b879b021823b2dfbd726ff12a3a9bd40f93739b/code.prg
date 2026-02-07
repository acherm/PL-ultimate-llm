* Simple Visual FoxPro program to demonstrate database operations
* Create a cursor (temporary table)
CREATE CURSOR employees (;
    emp_id I,;
    emp_name C(30),;
    department C(20),;
    salary N(10,2))

* Insert sample data
INSERT INTO employees VALUES (101, 'John Smith', 'Sales', 45000.00)
INSERT INTO employees VALUES (102, 'Jane Doe', 'Engineering', 65000.00)
INSERT INTO employees VALUES (103, 'Bob Johnson', 'Marketing', 50000.00)
INSERT INTO employees VALUES (104, 'Alice Williams', 'Engineering', 70000.00)

* Display all records
? "All Employees:"
? "=============="
SELECT * FROM employees INTO CURSOR results
SCAN
    ? TRANSFORM(emp_id) + " - " + ALLTRIM(emp_name) + ;
      " (" + ALLTRIM(department) + "): $" + ;
      TRANSFORM(salary, "@$ 999,999.99")
ENDSCAN

* Calculate average salary by department
? ""
? "Average Salary by Department:"
? "============================="
SELECT department, AVG(salary) AS avg_sal ;
    FROM employees ;
    GROUP BY department ;
    INTO CURSOR dept_avg

SCAN
    ? ALLTRIM(department) + ": $" + TRANSFORM(avg_sal, "@$ 999,999.99")
ENDSCAN

* Close cursors
USE IN employees
USE IN results
USE IN dept_avg
