; Fibonacci sequence in mIRC Script
alias fibonacci {
  var %n = $1
  if (%n <= 0) { return 0 }
  if (%n == 1) { return 1 }
  var %a = 0, %b = 1, %i = 2, %c
  while (%i <= %n) {
    %c = $calc(%a + %b)
    %a = %b
    %b = %c
    inc %i
  }
  return %b
}

alias show_fibonacci {
  var %i = 0
  while (%i <= 10) {
    echo -a Fibonacci( $+ %i $+ ) = $fibonacci(%i)
    inc %i
  }
}
