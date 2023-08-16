@echo off
cls

:: If the script receives a directory argument, set it as the current directory
if not "%~1"=="" (
    cd /d %~1
)

:: Store the current directory
set "currentDir=%cd%"
echo Current working directory detected: %currentDir%

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto gotAdmin
) else (
    goto requestAdmin
)

:requestAdmin
echo Requesting administrative privileges...
echo.

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
echo Set working directory back to: %currentDir%

:: If running with admin privileges, proceed with the script
echo Installing the requirements...
echo.
pip install -r requirements.txt

:: Check if requirements.txt was found and installed successfully
if %errorLevel% == 0 (
    echo Requirements install finised.
) else (
    echo ERROR: Could not install.
)

:: Pause at the end
pause
exit /b
