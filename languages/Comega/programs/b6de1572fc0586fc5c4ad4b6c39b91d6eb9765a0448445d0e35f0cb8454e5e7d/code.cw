using Microsoft.Comega;
using System;

public class Books{
  struct{
    string title;
    string author;
    string publisher;
    string? onloan;
  }* Book;

  public static void Main(){
    Books books = new Books();
    books.Book = new struct {title="Essential.NET", author="Don Box",
         publisher="Addison-Wesley", onloan = (string?) null};
    Console.WriteLine((string) books.Book.author + " is the author of " +
         (string) books.Book.title);
  }
}
