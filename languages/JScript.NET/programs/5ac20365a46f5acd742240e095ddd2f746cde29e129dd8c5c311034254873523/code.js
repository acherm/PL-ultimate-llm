import System;

class HelloWorld {
    static function Main() : void {
        var message : String = "Hello, World!";
        Console.WriteLine(message);

        // Demonstrate array usage
        var numbers : int[] = [1, 2, 3, 4, 5];
        var sum : int = 0;
        for (var i : int = 0; i < numbers.length; i++) {
            sum += numbers[i];
        }
        Console.WriteLine("Sum: " + sum);
    }
}

HelloWorld.Main();
