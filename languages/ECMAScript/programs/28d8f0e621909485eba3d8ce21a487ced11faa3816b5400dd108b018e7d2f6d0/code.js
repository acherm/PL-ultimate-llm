// ECMAScript example: Array manipulation and functional programming
const numbers = [1, 2, 3, 4, 5];

// Map operation
const doubled = numbers.map(n => n * 2);

// Filter operation
const evens = numbers.filter(n => n % 2 === 0);

// Reduce operation
const sum = numbers.reduce((acc, n) => acc + n, 0);

console.log('Original:', numbers);
console.log('Doubled:', doubled);
console.log('Evens:', evens);
console.log('Sum:', sum);
