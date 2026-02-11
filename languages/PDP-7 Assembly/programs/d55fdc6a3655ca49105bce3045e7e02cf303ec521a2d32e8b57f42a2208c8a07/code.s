   " Simple counter program
   lac d0     " Load accumulator with 0
   dac count  " Store in count variable

loop:
   lac count  " Load count
   add d1     " Add 1
   dac count  " Store back to count
   sad d10    " Skip if accumulator differs from 10
   hlt        " Halt if equal to 10
   jmp loop   " Jump back to loop

d0: 0          " Constant 0
d1: 1          " Constant 1
d10: 10        " Constant 10
count: 0       " Counter variable
