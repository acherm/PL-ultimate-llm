function f = fibonacci(n)
% Compute the nth Fibonacci number
  if (n == 0)
    f = 0;
  elseif (n == 1)
    f = 1;
  else
    f = fibonacci(n-1) + fibonacci(n-2);
  endif
endfunction

% Compute and display first 15 Fibonacci numbers
for i = 0:14
  printf('F(%d) = %d\n', i, fibonacci(i));
end
