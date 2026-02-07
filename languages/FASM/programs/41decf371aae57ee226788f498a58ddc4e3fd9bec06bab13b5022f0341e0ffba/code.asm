format PE console
entry start

include 'win32a.inc'

section '.data' data readable writeable
    hello db 'Hello, World!',0

section '.code' code readable executable
start:
    invoke  printf,hello
    invoke  ExitProcess,0

section '.idata' import data readable writeable
    library kernel32,'kernel32.dll',\
            msvcrt,'msvcrt.dll'

    import kernel32,\
           ExitProcess,'ExitProcess'

    import msvcrt,\
           printf,'printf'
