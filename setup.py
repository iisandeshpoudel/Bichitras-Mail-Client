from cx_Freeze import setup, Executable
import sys
import os

# Base directory of the project
BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Create empty templates.json if it doesn't exist
if not os.path.exists('templates.json'):
    with open('templates.json', 'w') as f:
        f.write('{}')

# Create empty logs directory
if not os.path.exists('logs'):
    os.makedirs('logs')

# Dependencies
build_exe_options = {
    "packages": [
        "PyQt6", 
        "email", 
        "smtplib", 
        "requests", 
        "json", 
        "dataclasses",
        "typing",
        "io"
    ],
    "excludes": [],
    "include_files": [
        # Include any additional resources
        "templates.json",
        "README.md",
        "LICENSE.txt",
        "icon.ico",
        ("gui", "gui"),  # Copy gui directory
        ("utils", "utils"),  # Copy utils directory
    ],
    "include_msvcr": True,  # Include Visual C++ runtime
}

# Target executable
target = Executable(
    script="main.py",
    base="Win32GUI" if sys.platform == "win32" else None,
    icon="icon.ico",
    target_name="BichitrasMailClient.exe",
    shortcut_name="Bichitras Mail Client",
    shortcut_dir="DesktopFolder",
    copyright="Copyright © 2024 Bichitras"
)

setup(
    name="BichitrasMailClient",
    version="1.0.0",
    description="Modern Mail Client for Bichitras",
    author="Bichitras",
    options={"build_exe": build_exe_options},
    executables=[target]
)
