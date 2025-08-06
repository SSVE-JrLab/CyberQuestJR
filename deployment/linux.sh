#!/bin/bash

# CyberQuest Jr - Linux/macOS Setup Script
# This script automatically sets up the entire project

echo "🛡️  CyberQuest Jr - Automated Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Python is installed
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    print_success "Python3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    print_success "Python found: $(python --version)"
else
    print_error "Python not found! Please install Python 3.8+ and try again."
    exit 1
fi

# Check if pip is installed
print_status "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    print_error "pip not found! Please install pip and try again."
    exit 1
fi
print_success "pip found"

# Check if Node.js is installed
print_status "Checking Node.js installation..."
if command -v node &> /dev/null; then
    print_success "Node.js found: $(node --version)"
else
    print_error "Node.js not found! Please install Node.js 16+ and try again."
    exit 1
fi

# Check if npm is installed
print_status "Checking npm installation..."
if command -v npm &> /dev/null; then
    print_success "npm found: $(npm --version)"
else
    print_error "npm not found! Please install npm and try again."
    exit 1
fi

print_status "All prerequisites found! Starting setup..."

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

# Setup Backend
print_status "Setting up backend dependencies..."
cd backend || exit 1

print_status "Installing Python packages..."
$PIP_CMD install fastapi uvicorn sqlalchemy python-dotenv openai

if [ $? -eq 0 ]; then
    print_success "Backend dependencies installed successfully!"
else
    print_error "Failed to install backend dependencies!"
    exit 1
fi

# Setup Frontend
print_status "Setting up frontend dependencies..."
cd ../frontend || exit 1

print_status "Installing npm packages..."
npm install

if [ $? -eq 0 ]; then
    print_success "Frontend dependencies installed successfully!"
else
    print_error "Failed to install frontend dependencies!"
    exit 1
fi

# Build Frontend
print_status "Building frontend..."
npm run build

if [ $? -eq 0 ]; then
    print_success "Frontend built successfully!"
else
    print_error "Failed to build frontend!"
    exit 1
fi

# Copy build files to backend
print_status "Copying build files to backend..."
cd .. || exit 1
cp -r frontend/dist backend/static

if [ $? -eq 0 ]; then
    print_success "Build files copied successfully!"
else
    print_error "Failed to copy build files!"
    exit 1
fi

# Create .env file if it doesn't exist
print_status "Setting up environment configuration..."
if [ ! -f backend/.env ]; then
    cat > backend/.env << EOF
# CyberQuest Jr Configuration
# Add your OpenAI API key below (optional - app works without it)
OPENAI_API_KEY=your_api_key_here

# Database
DATABASE_URL=sqlite:///./cyberquest.db
EOF
    print_success "Created .env file with default configuration"
    print_warning "Edit backend/.env to add your OpenAI API key (optional)"
else
    print_success ".env file already exists"
fi

# Create startup script
print_status "Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash
echo "🛡️  Starting CyberQuest Jr..."
cd backend
python3 app.py 2>/dev/null || python app.py
EOF

chmod +x start.sh

print_success "Setup completed successfully! 🎉"
echo ""
echo "🚀 To start the application:"
echo "   ./start.sh"
echo ""
echo "🌐 Then open your browser to:"
echo "   http://localhost:8000"
echo ""
echo "📝 Optional: Edit backend/.env to add OpenAI API key for enhanced features"
echo ""
print_success "Happy learning! 🛡️"
