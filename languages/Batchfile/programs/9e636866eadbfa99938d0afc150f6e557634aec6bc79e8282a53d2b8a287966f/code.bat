@echo off
setlocal enabledelayedexpansion

set /a "a=0, b=1"
echo Fibonacci sequence:
echo %a%
echo %b%

for /l %%i in (1,1,10) do (
    set /a "c=a+b"
    echo !c!
    set /a "a=b, b=c"
)
