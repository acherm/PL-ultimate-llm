CREATE KEYSPACE IF NOT EXISTS ybdemo;

USE ybdemo;

CREATE TABLE emp (
  emp_id INT PRIMARY KEY,
  emp_name TEXT,
  emp_age INT,
  emp_email TEXT
) WITH default_time_to_live = 0;

INSERT INTO emp (emp_id, emp_name, emp_age, emp_email)
  VALUES (1, 'John', 35, 'john@example.com');

INSERT INTO emp (emp_id, emp_name, emp_age, emp_email)
  VALUES (2, 'Jane', 28, 'jane@example.com');

INSERT INTO emp (emp_id, emp_name, emp_age, emp_email)
  VALUES (3, 'Bob', 42, 'bob@example.com');

SELECT * FROM emp;

SELECT emp_name, emp_email FROM emp WHERE emp_id = 1;

CREATE INDEX idx_emp_age ON emp (emp_age);

SELECT emp_name, emp_age FROM emp WHERE emp_age > 30 ALLOW FILTERING;
