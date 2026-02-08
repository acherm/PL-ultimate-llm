// Calculate factorial
PROCEDURE Factorial(n is int) : int

IF n <= 1 THEN
    RESULT 1
ELSE
    RESULT n * Factorial(n - 1)
END

// Main code
nValue is int = 5
Info("Factorial of " + nValue + " is " + Factorial(nValue))
