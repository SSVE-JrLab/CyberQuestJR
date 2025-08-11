#!/bin/bash

# CyberQuest Jr - Linux Deployment Script
# AI-Powered Cybersecurity Education Platform
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
clear
echo -e "${PURPLE}"
echo "██████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗███████╗███████╗████████╗    ██╗██████╗ "
echo "██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝    ██║██╔══██╗"
echo "██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║██║   ██║█████╗  ███████╗   ██║       ██║██████╔╝"
echo "██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║  ██   ██║██╔══██╗"
echo "╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╔╝╚██████╔╝███████╗███████║   ██║  ╚█████╔╝██║  ██║"
echo " ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚════╝ ╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${GREEN}🛡️  AI-Powered Cybersecurity Course Platform for Kids${NC}"
echo -e "${CYAN}🤖  Powered by Google Gemini AI${NC}"
echo "================================================================================"
echo ""

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if we're in the right directory
if [ ! -f "backend/app.py" ] || [ ! -f "frontend/package.json" ]; then
    print_error "Please run this script from the CyberQuestJR root directory"
    print_status "Expected structure:"
    echo "  CyberQuestJR/"
    echo "  ├── backend/"
    echo "  │   ├── app.py"
    echo "  │   └── requirements.txt"
    echo "  ├── frontend/"
    echo "  │   └── package.json"
    echo "  └── deployment/"
    echo "      └── linux.sh"
    exit 1
fi

print_status "🚀 Starting CyberQuest Jr deployment..."

# Check Python
print_status "Checking Python installation..."
if command_exists python3; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command_exists python; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    print_error "Python not found! Please install Python 3.8+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oP '\d+\.\d+')
print_success "Python $PYTHON_VERSION found"

# Check Node.js
print_status "Checking Node.js installation..."
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
else
    print_error "Node.js not found! Please install Node.js from https://nodejs.org"
    exit 1
fi

if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm $NPM_VERSION found"
else
    print_error "npm not found! Please install npm"
    exit 1
fi

# Install backend dependencies
print_status "📦 Installing Python dependencies..."
cd backend

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in backend directory!"
    exit 1
fi

# Install dependencies
$PIP_CMD install --upgrade pip
$PIP_CMD install -r requirements.txt --user

if [ $? -eq 0 ]; then
    print_success "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    print_warning "Try running: $PIP_CMD install --upgrade pip setuptools wheel"
    exit 1
fi

# Check environment file
print_status "🔧 Checking environment configuration..."
if [ ! -f ".env" ]; then
    print_warning "Creating .env file..."
    cat > .env << EOF
# Google Gemini AI Configuration
GEMINI_API_KEY=

# Database Configuration
DATABASE_URL=sqlite:///./cyberquest.db

# CORS Configuration
CORS_ALLOW_ORIGINS=*
EOF
    print_success ".env file created"
fi

# Check if API key is set
if ! grep -q "GEMINI_API_KEY=.\+" .env; then
    print_warning "⚠️  Google Gemini API key not configured!"
    echo ""
    echo -e "${YELLOW}To enable AI features:${NC}"
    echo "1. Visit https://ai.google.dev/ to get your API key"
    echo "2. Edit backend/.env and set: GEMINI_API_KEY=your_actual_key"
    echo ""
    print_status "Current .env file:"
    cat .env
    echo ""
    read -p "Press Enter to continue (AI features will use fallback content)..."
else
    print_success "Google Gemini API key configured ✨"
fi

cd ..

# Install frontend dependencies and build
print_status "📦 Installing Node.js dependencies..."
cd frontend

if [ ! -f "package.json" ]; then
    print_error "package.json not found in frontend directory!"
    exit 1
fi

npm install
if [ $? -eq 0 ]; then
    print_success "Node.js dependencies installed successfully"
else
    print_error "Failed to install Node.js dependencies"
    exit 1
fi

# Build frontend
print_status "🏗️  Building frontend..."
npm run build
if [ $? -eq 0 ]; then
    print_success "Frontend built successfully"
else
    print_error "Failed to build frontend"
    exit 1
fi

# Copy frontend build to backend static directory
print_status "📁 Copying frontend files to backend..."
cd ..
rm -rf backend/static
mkdir -p backend/static
cp -r frontend/dist/* backend/static/
print_success "Frontend files copied to backend/static"

# Create database
print_status "🗄️  Initializing database..."
cd backend
$PYTHON_CMD -c "
from app import Base, engine
Base.metadata.create_all(bind=engine)
print('Database initialized successfully')
"

if [ $? -eq 0 ]; then
    print_success "Database initialized"
else
    print_warning "Database initialization had issues (may already exist)"
fi

# Clean up any existing processes
print_status "🧹 Cleaning up existing processes..."
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
sleep 2

# Final setup
print_status "🎯 Final preparations..."

echo ""
echo -e "${GREEN}=================================================================================${NC}"
echo -e "${GREEN}🎉 CyberQuest Jr is ready to launch!${NC}"
echo -e "${GREEN}=================================================================================${NC}"
echo ""
echo -e "${CYAN}🤖 AI-Powered Cybersecurity Education Platform${NC}"
echo -e "${BLUE}🌐 Server starting at: ${YELLOW}http://localhost:8000${NC}"
echo -e "${PURPLE}🛡️  Features: Course Generation, Interactive Quizzes, Progress Tracking${NC}"
echo ""
echo -e "${YELLOW}📝 Controls:${NC}"
echo -e "   • ${GREEN}CTRL+C${NC} to stop the server"
echo -e "   • Check ${BLUE}http://localhost:8000${NC} in your browser"
echo ""
echo -e "${RED}Press CTRL+C to stop the server${NC}"
echo ""

# Start the server
print_status "🚀 Starting CyberQuest Jr server..."
echo ""
$PYTHON_CMD app.py

# Change to project root directory
cd "$(dirname "$0")/.."

print_status "Starting CyberQuest Jr setup..."

# Check system requirements
print_status "Checking system requirements..."

# Check Python
if command_exists python3; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
elif command_exists python; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python not found! Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
if command_exists pip3; then
    PIP_CMD="pip3"
elif command_exists pip; then
    PIP_CMD="pip"
else
    print_error "pip not found! Please install pip"
    exit 1
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
else
    print_warning "Node.js not found! Installing Node.js..."

    # Install Node.js based on distribution
    if command_exists apt; then
        # Ubuntu/Debian
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif command_exists yum; then
        # RHEL/CentOS
        curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
        sudo yum install -y nodejs npm
    elif command_exists pacman; then
        # Arch Linux
        sudo pacman -S nodejs npm
    else
        print_error "Cannot automatically install Node.js. Please install it manually from https://nodejs.org/"
        exit 1
    fi
fi

# Check npm
if command_exists npm; then
    NPM_VERSION=$(npm --version)
    print_success "npm $NPM_VERSION found"
else
    print_error "npm not found! Please install npm"
    exit 1
fi

# Check Python version compatibility
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 13 ]; then
    print_warning "Python 3.13+ detected. Some packages may have compatibility issues."
    print_status "Attempting installation with compatibility flags..."

    # Try to use older compatible versions for Python 3.13
    export PIP_NO_BUILD_ISOLATION=false
    export PIP_USE_PEP517=true
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
cd backend
if [ -f "requirements.txt" ]; then
    # For Python 3.13, try installing with specific flags
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 13 ]; then
        print_status "Using Python 3.13+ compatible installation method..."
        $PIP_CMD install --upgrade pip setuptools wheel
        $PIP_CMD install --no-cache-dir --force-reinstall "sqlalchemy>=2.0.35"
        $PIP_CMD install --no-cache-dir --force-reinstall "google-generativeai>=0.8.0"
        $PIP_CMD install --no-cache-dir --force-reinstall pydantic==2.10.3 pydantic-core==2.27.1
        $PIP_CMD install --no-cache-dir -r requirements.txt --user
    else
        # Install Google GenAI and updated SQLAlchemy first for compatibility
        $PIP_CMD install --upgrade "sqlalchemy>=2.0.35" "google-generativeai>=0.8.0"
        $PIP_CMD install -r requirements.txt --user
    fi

    if [ $? -eq 0 ]; then
        print_success "Python dependencies installed"
        print_success "Google GenAI integration ready!"
    else
        print_error "Failed to install Python dependencies"
        print_warning "If you're using Python 3.13, consider using Python 3.11 or 3.12 instead"
        print_warning "You can install Python 3.12 with: sudo apt install python3.12 python3.12-pip"
        exit 1
    fi
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Install Node.js dependencies and build frontend
print_status "Installing Node.js dependencies..."
cd ../frontend
if [ -f "package.json" ]; then
    npm install
    print_success "Node.js dependencies installed"

    print_status "Building frontend..."
    npm run build
    print_success "Frontend built successfully"

    # Copy build files to backend/static
    print_status "Copying frontend build to backend/static..."
    cd ..
    mkdir -p backend/static
    cp -r frontend/dist/* backend/static/
    print_success "Frontend files copied to backend/static"
else
    print_error "package.json not found!"
    exit 1
fi

# Go back to project root
cd backend

# Check environment configuration
print_status "Checking environment configuration..."
if [ -f ".env" ]; then
    # Check if Google GenAI API key is configured
    if grep -q "GEMINI_API_KEY=$" .env || ! grep -q "GEMINI_API_KEY=" .env; then
        print_warning "Google GenAI API key not configured!"
        echo "Please add your Google GenAI API key to backend/.env:"
        echo "1. Get your API key from https://ai.google.dev/"
        echo "2. Edit backend/.env and set GEMINI_API_KEY=your_actual_key"
        echo "3. Make sure you have access to the Gemini API"
        echo ""
        print_status "Current .env file content:"
        cat .env
        echo ""
        read -p "Press Enter to continue once you've added your API key..."
    else
        print_success "Environment configuration found"
        print_success "Google GenAI API key configured"
    fi
else
    print_warning "Environment file not found! Creating backend/.env..."
    echo "# Google GenAI Configuration" > .env
    echo "GEMINI_API_KEY=" >> .env
    echo "DATABASE_URL=sqlite:///./cyberquest_game.db" >> .env
    echo ""
    print_warning "Please add your Google GenAI API key to backend/.env"
    echo "1. Get your API key from https://ai.google.dev/"
    echo "2. Edit backend/.env and set GEMINI_API_KEY=your_actual_key"
    echo ""
    read -p "Press Enter to continue once you've added your API key..."
fi

# Clean up any existing processes
print_status "Cleaning up existing processes..."
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

# Start the unified server
print_status "Starting CyberQuest Jr unified server..."

echo ""
echo -e "${GREEN}🎮 Starting CyberQuest Jr Gaming Platform...${NC}"
echo -e "${BLUE}🤖 AI-powered cybersecurity education for kids${NC}"
echo -e "${YELLOW}🌐 Server will be available at: http://localhost:8000${NC}"
echo ""
echo -e "${PURPLE}Press CTRL+C to stop the server${NC}"
echo ""

# Start the server
$PYTHON_CMD app.py
