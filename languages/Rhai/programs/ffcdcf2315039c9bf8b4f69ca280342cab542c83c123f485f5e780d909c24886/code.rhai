// Fibonacci sequence in Rhai

fn fibonacci(n) {
    if n <= 0 {
        return 0;
    }
    if n == 1 {
        return 1;
    }

    let a = 0;
    let b = 1;

    for i in 2..=n {
        let temp = a + b;
        a = b;
        b = temp;
    }

    b
}

// Print the first 20 Fibonacci numbers
for i in 0..20 {
    let result = fibonacci(i);
    print("fibonacci(" + i + ") = " + result);
}
