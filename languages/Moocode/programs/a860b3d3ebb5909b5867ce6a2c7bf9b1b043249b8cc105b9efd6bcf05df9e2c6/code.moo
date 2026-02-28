"Print the first 10 Fibonacci numbers";
a = 0;
b = 1;
for i in [0..9]
  player:tell(tostr(a));
  temp = a + b;
  a = b;
  b = temp;
endfor
