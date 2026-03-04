#!/usr/bin/env gjs
'use strict';

// Fibonacci using GJS (GNOME JavaScript / SpiderMonkey)
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Print first 10 Fibonacci numbers
for (let i = 0; i <= 9; i++) {
    print('fibonacci(' + i + ') = ' + fibonacci(i));
}

// Generator-based approach
function* fibGen() {
    let [a, b] = [0, 1];
    while (true) {
        yield a;
        [a, b] = [b, a + b];
    }
}

const gen = fibGen();
const first10 = [];
for (let i = 0; i < 10; i++) {
    first10.push(gen.next().value);
}
print('Generator sequence: ' + first10.join(', '));
