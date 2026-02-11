<DEFINE FACTORIAL (N)
  <COND (<L? .N 2> 1)
        (T <* .N <FACTORIAL <- .N 1>>>)>>

<PRINC "Factorial of 5: ">
<PRINC <FACTORIAL 5>>
<PRINC "
">
