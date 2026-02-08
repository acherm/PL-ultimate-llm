<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron">
  <title>Book Validation Schema</title>

  <pattern>
    <rule context="book">
      <assert test="title">
        A book must have a title.
      </assert>
      <assert test="author">
        A book must have an author.
      </assert>
      <assert test="string-length(isbn) = 13 or string-length(isbn) = 10">
        ISBN must be either 10 or 13 characters long.
      </assert>
    </rule>

    <rule context="book/publication_year">
      <assert test=". &gt;= 1450 and . &lt;= 2030">
        Publication year must be between 1450 and 2030.
      </assert>
    </rule>

    <rule context="book/price">
      <assert test="@currency">
        Price must have a currency attribute.
      </assert>
      <assert test=". &gt; 0">
        Price must be greater than zero.
      </assert>
    </rule>
  </pattern>
</schema>
