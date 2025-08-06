@echo off
setlocal EnableDelayedExpansion

REM CyberQuest Jr - Windows Setup Script
REM This script automatically sets up the entire project

echo 🛡️  CyberQuest Jr - Automated Setup
echo ==================================
echo.

REM Function to print status messages
set "INFO_COLOR=[94m[INFO][0m"
set "SUCCESS_COLOR=[92m[SUCCESS][0m"
set "WARNING_COLOR=[93m[WARNING][0m"
set "ERROR_COLOR=[91m[ERROR][0m"

REM Check if Python is installed
echo %INFO_COLOR% Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    echo %SUCCESS_COLOR% Python found
) else (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py
        echo %SUCCESS_COLOR% Python found
    ) else (
        echo %ERROR_COLOR% Python not found! Please install Python 3.8+ from python.org
        pause
        exit /b 1
    )
)

REM Check if pip is installed
echo %INFO_COLOR% Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo %SUCCESS_COLOR% pip found
) else (
    echo %ERROR_COLOR% pip not found! Please install pip and try again.
    pause
    exit /b 1
)

REM Check if Node.js is installed
echo %INFO_COLOR% Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo %SUCCESS_COLOR% Node.js found
) else (
    echo %ERROR_COLOR% Node.js not found! Please install Node.js 16+ from nodejs.org
    pause
    exit /b 1
)

REM Check if npm is installed
echo %INFO_COLOR% Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% equ 0 (
    echo %SUCCESS_COLOR% npm found
) else (
    echo %ERROR_COLOR% npm not found! Please install npm and try again.
    pause
    exit /b 1
)

echo %INFO_COLOR% All prerequisites found! Starting setup...
echo.

REM Navigate to project root
cd /d "%~dp0\.."

REM Setup Backend
echo %INFO_COLOR% Setting up backend dependencies...
cd backend

echo %INFO_COLOR% Installing Python packages...
pip install fastapi uvicorn sqlalchemy python-dotenv openai

if %errorlevel% equ 0 (
    echo %SUCCESS_COLOR% Backend dependencies installed successfully!
) else (
    echo %ERROR_COLOR% Failed to install backend dependencies!
    pause
    exit /b 1
)

REM Setup Frontend
echo %INFO_COLOR% Setting up frontend dependencies...
cd ..\frontend

echo %INFO_COLOR% Installing npm packages...
npm install

if %errorlevel% equ 0 (
    echo %SUCCESS_COLOR% Frontend dependencies installed successfully!
) else (
    echo %ERROR_COLOR% Failed to install frontend dependencies!
    pause
    exit /b 1
)

REM Build Frontend
echo %INFO_COLOR% Building frontend...
npm run build

if %errorlevel% equ 0 (
    echo %SUCCESS_COLOR% Frontend built successfully!
) else (
    echo %ERROR_COLOR% Failed to build frontend!
    pause
    exit /b 1
)

REM Copy build files to backend
echo %INFO_COLOR% Copying build files to backend...
cd ..
xcopy frontend\dist backend\static /E /I /Y >nul 2>&1

if %errorlevel% equ 0 (
    echo %SUCCESS_COLOR% Build files copied successfully!
) else (
    echo %ERROR_COLOR% Failed to copy build files!
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
echo %INFO_COLOR% Setting up environment configuration...
if not exist backend\.env (
    echo # CyberQuest Jr Configuration > backend\.env
    echo # Add your OpenAI API key below (optional - app works without it) >> backend\.env
    echo OPENAI_API_KEY=your_api_key_here >> backend\.env
    echo. >> backend\.env
    echo # Database >> backend\.env
    echo DATABASE_URL=sqlite:///./cyberquest.db >> backend\.env
    echo %SUCCESS_COLOR% Created .env file with default configuration
    echo %WARNING_COLOR% Edit backend\.env to add your OpenAI API key (optional)
) else (
    echo %SUCCESS_COLOR% .env file already exists
)

REM Create startup script
echo %INFO_COLOR% Creating startup script...
echo @echo off > start.bat
echo echo 🛡️  Starting CyberQuest Jr... >> start.bat
echo cd backend >> start.bat
echo python app.py >> start.bat
echo pause >> start.bat

echo %SUCCESS_COLOR% Setup completed successfully! 🎉
echo.
echo 🚀 To start the application:
echo    start.bat
echo.
echo 🌐 Then open your browser to:
echo    http://localhost:8000
echo.
echo 📝 Optional: Edit backend\.env to add OpenAI API key for enhanced features
echo.
echo %SUCCESS_COLOR% Happy learning! 🛡️
echo.
pause
