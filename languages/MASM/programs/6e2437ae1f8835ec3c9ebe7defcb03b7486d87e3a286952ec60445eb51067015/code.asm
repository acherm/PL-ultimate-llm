.386
.model flat, stdcall
option casemap:none

includelib kernel32.lib
ExitProcess PROTO :DWORD
GetStdHandle PROTO :DWORD
WriteConsoleA PROTO :DWORD, :DWORD, :DWORD, :DWORD, :DWORD

.data
    msg db "Hello, World!", 13, 10
    msgLen equ $ - msg
    STD_OUTPUT_HANDLE equ -11

.data?
    hStdOut dd ?
    bytesWritten dd ?

.code
start:
    invoke GetStdHandle, STD_OUTPUT_HANDLE
    mov hStdOut, eax
    invoke WriteConsoleA, hStdOut, addr msg, msgLen, addr bytesWritten, 0
    invoke ExitProcess, 0
end start