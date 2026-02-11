#!/bin/csh

# purpose: demo foreach loop
# author: nixcraft
# -------------------------------

set n = 1
foreach i ( zebra ant bee cat )
  echo "Word $n is: $i"
  @ n++
end