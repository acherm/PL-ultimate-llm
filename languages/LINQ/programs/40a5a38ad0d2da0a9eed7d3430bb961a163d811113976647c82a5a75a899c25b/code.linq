// Basic LINQ query syntax demonstration
// Source: Microsoft LINQ documentation

int[] numbers = { 5, 10, 8, 3, 6, 12 };

// Query expression (declarative syntax)
IEnumerable<int> numQuery =
    from num in numbers
    where num % 2 == 0
    orderby num
    select num;

// Method syntax (equivalent)
IEnumerable<int> numQuery2 = numbers.Where(num => num % 2 == 0).OrderBy(n => n);

Console.Write("Query syntax:  ");
foreach (int i in numQuery)
    Console.Write(i + " ");

Console.Write("\nMethod syntax: ");
foreach (int i in numQuery2)
    Console.Write(i + " ");

Console.WriteLine();
