@echo off
mode 50,15
cls

:: If the script receives a directory argument, set it as the current directory
if not "%~1"=="" (
    cd /d %~1
)

:: Store the current directory
set "currentDir=%cd%"
echo Detected directory: %currentDir%

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto gotAdmin
) else (
    goto requestAdmin
)

:requestAdmin
echo Requesting admin rights...

:: Get the full path of the current batch script
setlocal
set "batchPath=%~f0"
echo Batch script path: %batchPath%
goto checkUAC

:checkUAC
echo Creating VBScript to request admin privileges...
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%batchPath%", "%currentDir%", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
exit /b

:gotAdmin
:: Set the working directory back to the original location
cd /d "%currentDir%"
echo Directory set to: %currentDir%
echo.

:: Run the freqbeat.py script
echo Launching FreqBeat...
echo.
python freqbeat.py
echo.
echo.

:: Exiting
echo FreqBeat shutting down...
echo.
echo.
pause
exit /b
