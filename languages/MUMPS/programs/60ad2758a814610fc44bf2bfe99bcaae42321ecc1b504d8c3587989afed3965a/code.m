HELLO
 ; Simple MUMPS program demonstrating basic I/O
 WRITE "Hello, World!",!
 WRITE "Enter your name: "
 READ NAME
 IF NAME'="" WRITE "Hello, ",NAME,"!",!
 WRITE "Today's date: "
 WRITE $ZDATE($HOROLOG,"DD-MON-YYYY"),!
 QUIT