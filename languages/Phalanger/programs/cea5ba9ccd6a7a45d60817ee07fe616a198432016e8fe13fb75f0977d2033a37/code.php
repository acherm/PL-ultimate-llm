<?php
// Phalanger example - Object-oriented PHP compiled to .NET
// Demonstrates class inheritance and .NET interop

class Animal {
    protected $name;
    protected $sound;

    public function __construct($name, $sound) {
        $this->name = $name;
        $this->sound = $sound;
    }

    public function speak() {
        echo $this->name . ' says ' . $this->sound . PHP_EOL;
    }

    public function getName() {
        return $this->name;
    }
}

class Dog extends Animal {
    private $breed;

    public function __construct($name, $breed) {
        parent::__construct($name, 'Woof');
        $this->breed = $breed;
    }

    public function fetch($item) {
        echo $this->name . ' fetches the ' . $item . '!' . PHP_EOL;
    }

    public function describe() {
        echo $this->name . ' is a ' . $this->breed . ' dog.' . PHP_EOL;
    }
}

class Cat extends Animal {
    public function __construct($name) {
        parent::__construct($name, 'Meow');
    }

    public function purr() {
        echo $this->name . ' purrs contentedly.' . PHP_EOL;
    }
}

// Create instances
$dog = new Dog('Rex', 'German Shepherd');
$cat = new Cat('Whiskers');

// Demonstrate polymorphism
$animals = array($dog, $cat);
foreach ($animals as $animal) {
    $animal->speak();
}

// Dog-specific methods
$dog->describe();
$dog->fetch('ball');

// Cat-specific methods
$cat->purr();

// Using PHP_INT_MAX (a .NET platform constant in Phalanger)
echo 'Max integer: ' . PHP_INT_MAX . PHP_EOL;
echo 'Animal count: ' . count($animals) . PHP_EOL;
