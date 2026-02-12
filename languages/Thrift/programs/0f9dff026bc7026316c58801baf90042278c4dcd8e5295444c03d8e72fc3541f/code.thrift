namespace java com.example.calculator
namespace py calculator

typedef i32 int

enum Operation {
  ADD = 1,
  SUBTRACT = 2,
  MULTIPLY = 3,
  DIVIDE = 4
}

exception InvalidOperationException {
  1: int errorCode,
  2: string message
}

struct Work {
  1: int num1 = 0,
  2: int num2,
  3: Operation op,
  4: optional string comment
}

service Calculator {
  int add(1:int num1, 2:int num2),
  int calculate(1:int logid, 2:Work w) throws (1:InvalidOperationException ouch),
  oneway void zip()
}
