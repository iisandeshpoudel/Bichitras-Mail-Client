@echo off
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo Installing requirements...
pip install -r requirements.txt

echo Creating icon...
python utils/create_icon.py

echo Creating single standalone executable...
pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data "templates.json;." ^
    --add-data "gui;gui" ^
    --add-data "utils;utils" ^
    --add-data "icon.ico;." ^
    --name "BichitrasMailClient" ^
    --clean ^
    --noupx ^
    --runtime-tmpdir "." ^
    --hidden-import "PyQt6.QtCore" ^
    --hidden-import "PyQt6.QtGui" ^
    --hidden-import "PyQt6.QtWidgets" ^
    main.py

echo Cleaning up...
if exist build rmdir /s /q build
if exist *.spec del /f /q *.spec

echo Done!
echo Single portable executable is in: dist/BichitrasMailClient.exe
pause
