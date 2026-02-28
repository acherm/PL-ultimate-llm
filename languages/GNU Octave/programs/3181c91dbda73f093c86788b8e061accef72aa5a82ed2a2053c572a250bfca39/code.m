% Compute first N Fibonacci numbers iteratively
function fibs = fibonacci(n)
  fibs = zeros(1, n);
  fibs(1) = 1;
  if n > 1
    fibs(2) = 1;
    for i = 3:n
      fibs(i) = fibs(i-1) + fibs(i-2);
    end
  end
endfunction

n = 10;
result = fibonacci(n);
printf("First %d Fibonacci numbers:\n", n);
disp(result)
