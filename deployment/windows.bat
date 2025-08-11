@echo off
setlocal enabledelayedexpansion

rem CyberQuest Jr - Windows Deployment Script
rem AI-Powered Cybersecurity Education Platform

title CyberQuest Jr - Deployment

echo.
echo ████████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗███████╗███████╗████████╗    ██╗██████╗
echo ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝    ██║██╔══██╗
echo ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║██║   ██║█████╗  ███████╗   ██║       ██║██████╔╝
echo ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║  ██   ██║██╔══██╗
echo ╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╔╝╚██████╔╝███████╗███████║   ██║  ╚█████╔╝██║  ██║
echo  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚════╝ ╚═╝  ╚═╝
echo.
echo 🛡️  AI-Powered Cybersecurity Course Platform for Kids
echo 🤖  Powered by Google Gemini AI
echo ================================================================================
echo.

rem Check if we're in the right directory
if not exist "backend\app.py" (
    echo [ERROR] Please run this script from the CyberQuestJR root directory
    echo Expected structure:
    echo   CyberQuestJR\
    echo   ├── backend\
    echo   │   ├── app.py
    echo   │   └── requirements.txt
    echo   ├── frontend\
    echo   │   └── package.json
    echo   └── deployment\
    echo       └── windows.bat
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo [ERROR] Frontend package.json not found!
    pause
    exit /b 1
)

echo [INFO] 🚀 Starting CyberQuest Jr deployment...

rem Check Python
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python not found! Please install Python 3.8+ from https://python.org
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
        set PIP_CMD=py -m pip
    )
) else (
    set PYTHON_CMD=python
    set PIP_CMD=pip
)

for /f "tokens=2" %%i in ('%PYTHON_CMD% --version') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% found

rem Check Node.js
echo [INFO] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo [SUCCESS] Node.js %NODE_VERSION% found

npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm not found! Please install npm
    pause
    exit /b 1
)

for /f "tokens=1" %%i in ('npm --version') do set NPM_VERSION=%%i
echo [SUCCESS] npm %NPM_VERSION% found

rem Install backend dependencies
echo [INFO] 📦 Installing Python dependencies...
cd backend

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found in backend directory!
    pause
    exit /b 1
)

rem Install dependencies
%PIP_CMD% install --upgrade pip
%PIP_CMD% install -r requirements.txt --user

if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    echo [WARNING] Try running: %PIP_CMD% install --upgrade pip setuptools wheel
    pause
    exit /b 1
)

echo [SUCCESS] Python dependencies installed successfully

rem Check environment file
echo [INFO] 🔧 Checking environment configuration...
if not exist ".env" (
    echo [WARNING] Creating .env file...
    (
        echo # Google Gemini AI Configuration
        echo GEMINI_API_KEY=
        echo.
        echo # Database Configuration
        echo DATABASE_URL=sqlite:///./cyberquest.db
        echo.
        echo # CORS Configuration
        echo CORS_ALLOW_ORIGINS=*
    ) > .env
    echo [SUCCESS] .env file created
)

rem Check if API key is set
findstr /C:"GEMINI_API_KEY=" .env | findstr /V /C:"GEMINI_API_KEY=$" | findstr /V /C:"GEMINI_API_KEY= " >nul
if errorlevel 1 (
    echo [WARNING] ⚠️  Google Gemini API key not configured!
    echo.
    echo To enable AI features:
    echo 1. Visit https://ai.google.dev/ to get your API key
    echo 2. Edit backend\.env and set: GEMINI_API_KEY=your_actual_key
    echo.
    echo Current .env file:
    type .env
    echo.
    pause
) else (
    echo [SUCCESS] Google Gemini API key configured ✨
)

cd ..

rem Install frontend dependencies and build
echo [INFO] 📦 Installing Node.js dependencies...
cd frontend

if not exist "package.json" (
    echo [ERROR] package.json not found in frontend directory!
    pause
    exit /b 1
)

call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo [SUCCESS] Node.js dependencies installed successfully

rem Build frontend
echo [INFO] 🏗️  Building frontend...
call npm run build
if errorlevel 1 (
    echo [ERROR] Failed to build frontend
    pause
    exit /b 1
)

echo [SUCCESS] Frontend built successfully

rem Copy frontend build to backend static directory
echo [INFO] 📁 Copying frontend files to backend...
cd ..
if exist "backend\static" rmdir /s /q "backend\static"
mkdir "backend\static"
xcopy "frontend\dist\*" "backend\static\" /s /e /y >nul
echo [SUCCESS] Frontend files copied to backend\static

rem Create database
echo [INFO] 🗄️  Initializing database...
cd backend
%PYTHON_CMD% -c "from app import Base, engine; Base.metadata.create_all(bind=engine); print('Database initialized successfully')"

if errorlevel 1 (
    echo [WARNING] Database initialization had issues (may already exist)
) else (
    echo [SUCCESS] Database initialized
)

rem Clean up any existing processes
echo [INFO] 🧹 Cleaning up existing processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im py.exe >nul 2>&1
timeout /t 2 /nobreak >nul

rem Final setup
echo [INFO] 🎯 Final preparations...

echo.
echo =================================================================================
echo 🎉 CyberQuest Jr is ready to launch!
echo =================================================================================
echo.
echo 🤖 AI-Powered Cybersecurity Education Platform
echo 🌐 Server starting at: http://localhost:8000
echo 🛡️  Features: Course Generation, Interactive Quizzes, Progress Tracking
echo.
echo 📝 Controls:
echo    • CTRL+C to stop the server
echo    • Check http://localhost:8000 in your browser
echo.
echo Press CTRL+C to stop the server
echo.

rem Start the server
echo [INFO] 🚀 Starting CyberQuest Jr server...
echo.
%PYTHON_CMD% app.py
