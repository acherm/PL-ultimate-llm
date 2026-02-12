# Factorial function in NQP
sub factorial($n) {
    if $n <= 1 {
        return 1;
    }
    else {
        return $n * factorial($n - 1);
    }
}

# Print factorials from 1 to 10
for (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) -> $i {
    say("Factorial of $i is " ~ factorial($i));
}
