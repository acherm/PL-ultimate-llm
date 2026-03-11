(* Machiavelli: A polymorphic database programming language
   Example of record polymorphism and comprehension syntax *)

val employees =
  [{name = "Alice", dept = "CS",   salary = 50000},
   {name = "Bob",   dept = "Math", salary = 45000},
   {name = "Carol", dept = "CS",   salary = 55000},
   {name = "Dave",  dept = "Math", salary = 48000}];

(* Select employees by department using comprehension syntax *)
fun select_dept d table =
  [row | row <- table, row.dept = d];

(* Sum all salary fields using record polymorphism *)
fun sum_salary [] = 0
  | sum_salary (r :: rs) = r.salary + sum_salary rs;

val cs_employees = select_dept "CS" employees;
val cs_salary_total = sum_salary cs_employees;
