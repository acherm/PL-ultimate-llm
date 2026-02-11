MCSKIP "WITH" NL
"" ML/I Version 1.1 Example Program
MCSKIP MT,<>
MCINS %.
MCDEF SL SPACES NL AS <MCSET T1=%A1.
MCSET T2=1
%L1.MCGO L2 IF T2 GR T1
 MCGO L1
MCSET T2=T2+1
%L2.MCEND>
"" Demonstrate macro definition
Hello, World!
SL 5
This is ML/I
