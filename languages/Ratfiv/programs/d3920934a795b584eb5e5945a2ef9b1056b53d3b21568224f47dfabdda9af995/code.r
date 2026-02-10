# Factorial function in Ratfiv
function fact(n)
    integer n, i, result

    if (n <= 1) {
        return(1)
    }

    result = 1
    for (i = 2; i <= n; i = i + 1) {
        result = result * i
    }

    return(result)
end
