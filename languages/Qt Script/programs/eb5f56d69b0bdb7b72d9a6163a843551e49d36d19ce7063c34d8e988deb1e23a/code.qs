function Person(name, age) {
    this.name = name;
    this.age = age;
}

Person.prototype.greet = function() {
    print("Hello, my name is " + this.name + " and I am " + this.age + " years old.");
}

Person.prototype.toString = function() {
    return this.name + " (age " + this.age + ")";
}

var people = [
    new Person("Alice", 30),
    new Person("Bob", 25),
    new Person("Charlie", 35)
];

for (var i = 0; i < people.length; i++) {
    people[i].greet();
}
print("People: " + people.join(", "));
