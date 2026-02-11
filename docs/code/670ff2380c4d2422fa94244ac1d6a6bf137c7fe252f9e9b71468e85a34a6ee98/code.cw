// Example 3: Asynchronous methods with return values and chords.

using System;
using System.Threading;

public class Example {

  public static async int A() {
    Console.WriteLine("A starting");
    Thread.Sleep(1000);
    Console.WriteLine("A finishing");
    return 1;
  }

  public static async int B() {
    Console.WriteLine("B starting");
    Thread.Sleep(1000);
    Console.WriteLine("B finishing");
    return 2;
  }

  public static void Main() {
    Console.WriteLine("Main starting");
    async {
      int x = A();
      int y = B();
    } & {
      Console.WriteLine("Main got values");
      Console.WriteLine("x=" + x);
      Console.WriteLine("y=" + y);
    }
    Console.WriteLine("Main finishing");
  }
}