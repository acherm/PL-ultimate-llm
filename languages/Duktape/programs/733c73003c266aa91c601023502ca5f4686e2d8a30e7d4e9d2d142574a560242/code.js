// Duktape example: prime sieve using ECMAScript 5.1
// Demonstrates basic Duktape scripting capabilities

function sieve(limit) {
    var composite = [];
    var primes = [];
    var i, j;

    for (i = 2; i <= limit; i++) {
        if (!composite[i]) {
            primes.push(i);
            for (j = i * i; j <= limit; j += i) {
                composite[j] = true;
            }
        }
    }
    return primes;
}

var result = sieve(100);
print("Primes up to 100:");
print(result.join(", "));
print("Count: " + result.length);
