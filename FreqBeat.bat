@echo off
mode 65,20
rem con:cols=65 lines=65
cls

:: Set the current directory
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

:: Get path of batch script
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
:: Set the working directory
cd /d "%currentDir%"
echo Directory set to: %currentDir%
echo.

:: Ascii Art
echo " ___________                    __________               __    "
echo " \_   _____/______   ____  _____\______   \ ____ _____ _/  |_  "
echo "  |    __) \_  __ \_/ __ \/ ____/|    |  _// __ \\__  \\   __\ "
echo "  |     \   |  | \/\  ___< <_|  ||    |   \  ___/ / __ \|  |   "
echo "  \___  /   |__|    \___  >__   ||______  /\___  >____  /__|   "
echo "      \/                \/   |__|       \/     \/     \/       "
echo.
echo.

:: Run the freqbeat.py script
echo Launching FreqBeat...
echo.
@echo on
python freqbeat.py
@echo off
echo.
echo.

:: Exiting
echo FreqBeat shutting down...
echo.
echo.
pause
exit /b
