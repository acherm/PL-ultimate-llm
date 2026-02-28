// E4X - ECMAScript for XML (ECMA-357)
// Demonstrates XML literals and E4X operations

var catalog = <catalog>
  <book id="1">
    <title>JavaScript: The Good Parts</title>
    <author>Douglas Crockford</author>
    <price>29.99</price>
    <category>Programming</category>
  </book>
  <book id="2">
    <title>Learning XML</title>
    <author>Erik T. Ray</author>
    <price>39.99</price>
    <category>XML</category>
  </book>
  <book id="3">
    <title>Ajax: The Definitive Guide</title>
    <author>Anthony T. Holdener III</author>
    <price>49.99</price>
    <category>Programming</category>
  </book>
</catalog>;

// Access elements via dot notation
print("First book: " + catalog.book[0].title);

// Filter books by category using predicate
var programmingBooks = catalog.book.(@category == "Programming");
print("Programming books:");
for each (var book in programmingBooks) {
    print("  " + book.title + " by " + book.author);
}

// Compute total price
var total = 0;
for each (var b in catalog.book) {
    total += parseFloat(b.price);
}
print("Total price: $" + total.toFixed(2));

// Add a new book using XML literal
var newBook = <book id="4">
  <title>E4X in Action</title>
  <author>Sam Ruby</author>
  <price>34.99</price>
  <category>XML</category>
</book>;
catalog.appendChild(newBook);
print("Catalog now has " + catalog.book.length() + " books");
