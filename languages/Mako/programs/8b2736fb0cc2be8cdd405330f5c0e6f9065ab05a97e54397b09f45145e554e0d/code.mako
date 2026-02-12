<%!
    def fibonacci(n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b
%>

<!DOCTYPE html>
<html>
<head>
    <title>Fibonacci Numbers</title>
</head>
<body>
    <h1>First 10 Fibonacci Numbers</h1>
    <ul>
    % for i in range(10):
        <li>${i}: ${fibonacci(i)}</li>
    % endfor
    </ul>
</body>
</html>
