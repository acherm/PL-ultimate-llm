#!/usr/bin/env kotlin

// Compute Fibonacci numbers using Kotlin Script
fun fibonacci(n: Int): Sequence<Long> = sequence {
    var a = 0L
    var b = 1L
    repeat(n) {
        yield(a)
        val next = a + b
        a = b
        b = next
    }
}

val count = 20
println("First $count Fibonacci numbers:")
fibonacci(count).forEachIndexed { i, v ->
    println("  F($i) = $v")
}
