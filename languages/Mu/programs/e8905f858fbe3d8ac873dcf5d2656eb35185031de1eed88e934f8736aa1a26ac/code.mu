fn main -> exit-status/ebx: int {
  print-string 0, "Hello, Mu!\n"
  exit-status <- copy 0
}
