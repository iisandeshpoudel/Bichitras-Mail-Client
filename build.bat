@echo off
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist installer rmdir /s /q installer
if exist portable rmdir /s /q portable

echo Installing requirements...
pip install -r requirements.txt pillow

echo Creating icon...
python utils/create_icon.py

echo Ensuring required files exist...
if not exist templates.json (
    echo {} > templates.json
)
if not exist logs (
    mkdir logs
)

echo Building executable...
python setup.py build
if errorlevel 1 (
    echo Error building executable
    pause
    exit /b 1
)

echo Creating portable version...
mkdir portable\BichitrasMailClient
xcopy /E /I /Y build\exe.win-amd64-3.12\* portable\BichitrasMailClient\
copy /Y icon.ico portable\BichitrasMailClient\
copy /Y README.md portable\BichitrasMailClient\
copy /Y LICENSE.txt portable\BichitrasMailClient\
copy /Y templates.json portable\BichitrasMailClient\

echo Creating installer...
mkdir installer
:: Check for Inno Setup in different possible locations
SET "INNO_SETUP_PATH="
IF EXIST "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    SET "INNO_SETUP_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) ELSE IF EXIST "C:\Program Files\Inno Setup 6\ISCC.exe" (
    SET "INNO_SETUP_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
)

IF NOT DEFINED INNO_SETUP_PATH (
    echo Error: Inno Setup not found!
    echo Please download and install Inno Setup from: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

"%INNO_SETUP_PATH%" installer.iss
if errorlevel 1 (
    echo Error creating installer
    pause
    exit /b 1
)

echo Done!
echo Portable version is in: portable\BichitrasMailClient
echo Installer is in: installer\BichitrasMailClient_Setup.exe
pause
