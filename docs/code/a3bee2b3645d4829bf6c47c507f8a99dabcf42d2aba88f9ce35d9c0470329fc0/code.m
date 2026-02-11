% Fibonacci sequence generator
function fib = fibonacci(n)
    if n <= 0
        fib = [];
    elseif n == 1
        fib = 1;
    elseif n == 2
        fib = [1, 1];
    else
        fib = zeros(1, n);
        fib(1) = 1;
        fib(2) = 1;
        for i = 3:n
            fib(i) = fib(i-1) + fib(i-2);
        end
    end
end

% Generate first 15 Fibonacci numbers
n = 15;
fib_sequence = fibonacci(n);

% Display the sequence
disp('Fibonacci sequence:');
disp(fib_sequence);

% Plot the sequence
plot(1:n, fib_sequence, '-o', 'LineWidth', 2);
xlabel('Position');
ylabel('Fibonacci Number');
title('Fibonacci Sequence');
grid on;
