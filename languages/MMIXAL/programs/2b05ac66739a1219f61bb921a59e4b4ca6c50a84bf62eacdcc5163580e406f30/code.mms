* Hello World in MMIXAL
* Prints "Hello, World!" to standard output

        LOC  #100
Main    GETA $255,String
        TRAP 0,Fputs,StdOut
        TRAP 0,Halt,0

String  BYTE "Hello, World!",#a,0

        LOC  @+1000
