@echo off
mode 80,20
rem mode con:cols=65 lines=100
rem title StatStream
cls


:: Ascii Art
echo.
echo "    _________ __          __   _________ __                                   "
echo "   /   _____//  |______ _/  |_/   _____//  |________   ____ _____    _____    "
echo "   \_____  \\   __\__  \\   __\_____  \\   __\_  __ \_/ __ \\__  \  /     \   "
echo "   /        \|  |  / __ \|  | /        \|  |  |  | \/\  ___/ / __ \|  Y Y  \  "
echo "  /_______  /|__| |____  /__|/_______  /|__|  |__|    \___ \|____  /__|_|  /  "
echo "          \/           \/            \/                   \/     \/      \/   "
echo.
echo "                      Its time to stream those stats!"
timeout /t 3 /nobreak >nul
echo.
echo.


:: Run the freqbeat.py script
echo Launching StatStream...
echo.
@echo on
python main.py
@echo off
echo.
echo.

:: Exiting
echo StatStream shutting down...
echo.
echo.
pause
exit /b
