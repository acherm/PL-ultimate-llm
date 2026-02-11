// @flow
function add(a: number, b: number): number {
  return a + b;
}

function greet(name: string): string {
  return `Hello, ${name}!`;
}

type Person = {
  name: string,
  age: number,
};

function formatPerson(person: Person): string {
  return `${person.name} is ${person.age} years old`;
}

const result: number = add(5, 10);
const message: string = greet("World");
const john: Person = { name: "John", age: 30 };
const info: string = formatPerson(john);

console.log(result);
console.log(message);
console.log(info);
