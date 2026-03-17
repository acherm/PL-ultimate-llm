<result>
  FOR $author IN document("bib.xml")//author
  LET $books := document("bib.xml")//book[author = $author]
  WHERE count($books) > 1
  RETURN
    <prolific-author name="{ $author }">
      FOR $b IN $books
      RETURN
        <title>{ $b/title/text() }</title>
    </prolific-author>
</result>
