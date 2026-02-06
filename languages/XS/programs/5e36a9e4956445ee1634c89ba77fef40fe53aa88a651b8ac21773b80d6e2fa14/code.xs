#include "EXTERN.h"
#include "perl.h"
#include "XSUB.h"

MODULE = Example::Math  PACKAGE = Example::Math

int
add(a, b)
    int a
    int b
  CODE:
    RETVAL = a + b;
  OUTPUT:
    RETVAL

int
multiply(a, b)
    int a
    int b
  CODE:
    RETVAL = a * b;
  OUTPUT:
    RETVAL
