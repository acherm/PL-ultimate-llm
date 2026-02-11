$! LOGIN.COM
$!
$! This is a sample login command file.
$!
$! Set the prompt to show the current directory.
$ SET PROMPT="''F$GETDVI("DEFAULT","FULLNAME")' $ "
$!
$! Define some useful symbols.
$ H == "HELP"
$ D == "DIRECTORY"
$ DEL == "DELETE/CONFIRM"
$ PUR == "PURGE"
$ TY == "TYPE"
$ SE == "SET"
$ SH == "SHOW"
$!
$! Define some useful foreign commands.
$ PICO :== "$PICO"
$ PINE :== "$PINE"
$ KERMIT :== "$KERMIT"
$!
$! Show the time.
$ SHOW TIME
$!
$! Say hello.
$ WRITE SYS$OUTPUT "Hello, ''F$GETJPI("","USERNAME")'!"
$ WRITE SYS$OUTPUT "Welcome to CUVMS."