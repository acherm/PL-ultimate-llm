import std.os.*;
import std.convert.*;

main() {
  var maxn = Int.parse(if (let Some(v) <- getEnv("MAXN")) { v } else { "10" })
  var sum = 0
  for (i in 1..(maxn+1)) {
    sum += collatz(i)
  }
  println("sum=${sum}")
}

func collatz(n: Int): Int {
  var cnt = 0
  var res = n
  while (res > 1) {
    res = if (res % 2 > 0) {
      res * 3 + 1
    } else {
      res / 2
    }
    cnt++
  }
  return cnt
}
