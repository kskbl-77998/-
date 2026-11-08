@echo off
rem ============================================================
rem  Complement Simulator launcher
rem  Double-click this file to start the program.
rem  (File content is ASCII on purpose: non-ASCII text in .bat
rem   files breaks cmd.exe parsing on Chinese Windows.)
rem ============================================================
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 goto try_python
py -3 main.py
goto check

:try_python
where python >nul 2>nul
if errorlevel 1 goto no_python
python main.py
goto check

:no_python
echo.
echo [ERROR] Python not found.
echo Install Python 3.8+ from https://www.python.org/downloads/
echo Remember to tick "Add python.exe to PATH" during install.
echo.
pause
exit /b 1

:check
if errorlevel 1 (
    echo.
    echo [ERROR] Program exited abnormally. Copy the message above to the team lead.
    echo.
    pause
)
