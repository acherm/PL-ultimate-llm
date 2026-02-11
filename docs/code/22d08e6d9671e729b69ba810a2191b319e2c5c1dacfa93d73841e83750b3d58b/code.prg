* Program....: DBINFO.PRG
* Version....: 1.0
* Author.....: J.F.Ludwig
* Date.......: 01-01-96
* Notice.....: Copyright (c) 1996 J.F.Ludwig, All Rights Reserved.
* Notes......: This program displays database information
* ...........: for the database in the current work area.
* ...........:
*
* See also...: FLDINFO.PRG
* ...........:
*
* Updates....:
* ...........:
*
***********************************************************************

clear
? "Database information for: " + dbf()
? "Number of records.........: " + ltrim(str(reccount()))
? "Date of last update.......: " + dtoc(lupdate())
? "Number of fields..........: " + ltrim(str(fcount()))
? "Record size...............: " + ltrim(str(recsize()))
?
? "Memo file exists..........: " + iif(file(substr(dbf(),1,rat(".",dbf()))+"dbt"), "Yes", "No")
? "Is database encrypted.....: " + iif(isencrypted(), "Yes", "No")
? "Is database read only.....: " + iif(isreadonly(), "Yes", "No")
? "MDX file exists...........: " + iif(file(mdx(1)), "Yes", "No")
?
return