typeside Ty = literal {
  java_types
    String -> "java.lang.String"
    Integer -> "java.lang.Integer"
  java_constants
    String -> "return input[0]"
    Integer -> "return Integer.parseInt(input[0])"
}

schema S = literal : Ty {
  entities
    Employee
    Department
  foreign_keys
    worksIn : Employee -> Department
  attributes
    empName  : Employee -> String
    salary   : Employee -> Integer
    deptName : Department -> String
}

instance I = literal : S {
  generators
    alice bob : Employee
    eng hr    : Department
  equations
    worksIn(alice) = eng
    worksIn(bob) = hr
    empName(alice) = Alice
    salary(alice) = 75000
    empName(bob) = Bob
    salary(bob) = 80000
    deptName(eng) = Engineering
    deptName(hr) = HumanResources
}
