* Hello World and counter in dBASE II
* Classic business database language by Ashton-Tate (1981)
SET TALK OFF
STORE 1 TO M:I
? "Hello, World!"
?
DO WHILE M:I <= 5
   ? "Count:", M:I
   STORE M:I + 1 TO M:I
ENDDO
? "Done."
RETURN
