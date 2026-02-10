func.func @add(%arg0: i32, %arg1: i32) -> i32 {
  %0 = arith.addi %arg0, %arg1 : i32
  func.return %0 : i32
}

func.func @main() {
  %c1 = arith.constant 1 : i32
  %c2 = arith.constant 2 : i32
  %result = func.call @add(%c1, %c2) : (i32, i32) -> i32
  func.return
}
