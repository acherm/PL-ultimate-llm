@echo off

:Start
cls
echo.
echo 1. Option one
echo 2. Option two
echo.
set /p op=Please choose an option and press ENTER (1 or 2):
if %op%==1 goto one
if %op%==2 goto two
echo.
echo That is not a valid option. Please try again.
pause
goto Start

:one
echo.
echo You chose option 1
pause
goto end

:two
echo.
echo You chose option 2
pause
goto end

:end