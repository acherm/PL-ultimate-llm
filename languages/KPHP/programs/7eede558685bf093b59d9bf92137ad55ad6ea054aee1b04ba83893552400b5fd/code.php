<?php

function fibonacci(int $n): int {
    if ($n <= 1) {
        return $n;
    }
    return fibonacci($n - 1) + fibonacci($n - 2);
}

for ($i = 0; $i <= 10; $i++) {
    echo "fibonacci($i) = " . fibonacci($i) . "\n";
}
