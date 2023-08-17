@echo off
mode 65,20
mode con:cols=65 lines=100
cls

:: Ascii Art
echo " ___________                    __________               __    "
echo " \_   _____/______   ____  _____\______   \ ____ _____ _/  |_  "
echo "  |    __) \_  __ \_/ __ \/ ____/|    |  _// __ \\__  \\   __\ "
echo "  |     \   |  | \/\  ___< <_|  ||    |   \  ___/ / __ \|  |   "
echo "  \___  /   |__|    \___  >__   ||______  /\___  >____  /__|   "
echo "      \/                \/   |__|       \/     \/     \/       "
echo "                    Its time to get freqy!"
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
