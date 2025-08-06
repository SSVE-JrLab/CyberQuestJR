# 🛡️ CyberQuest Jr

**A fun and interactive cybersecurity education platform for kids aged 8-18!**

## ✨ Features

- 🎮 **Interactive Quizzes** - Learn cybersecurity through engaging quizzes
- 📚 **Learning Modules** - Structured lessons on digital safety
- 🏆 **Leaderboard** - Compete with friends and track progress
- 🌙 **Dark/Light Mode** - Beautiful themes for any time of day
- 🎨 **Kid-Friendly Design** - Colorful, intuitive interface
- 🔐 **No Authentication** - Jump right in and start learning!

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Linux/macOS:**
```bash
git clone https://github.com/Aarav2709/CyberQuestJR.git
cd CyberQuestJR
chmod +x deployment/setup-linux.sh
./deployment/setup-linux.sh
./start.sh
```

**Windows:**
1. Clone or download the repository
2. Double-click `deployment/setup-windows.bat`
3. Double-click `start.bat`

### Option 2: Manual Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aarav2709/CyberQuestJR.git
   cd CyberQuestJR
   ```

2. **Setup Backend**
   
   **Linux/macOS:**
   ```bash
   cd backend
   pip install fastapi uvicorn sqlalchemy python-dotenv openai
   ```
   
   **Windows:**
   ```cmd
   cd backend
   pip install fastapi uvicorn sqlalchemy python-dotenv openai
   ```

3. **Setup Frontend**
   
   **Linux/macOS:**
   ```bash
   cd ../frontend
   npm install
   npm run build
   ```
   
   **Windows:**
   ```cmd
   cd ..\frontend
   npm install
   npm run build
   ```

4. **Copy Build Files**
   
   **Linux/macOS:**
   ```bash
   cd ..
   cp -r frontend/dist backend/static
   ```
   
   **Windows:**
   ```cmd
   cd ..
   xcopy frontend\dist backend\static /E /I
   ```

5. **Start the Server**
   
   **Linux/macOS:**
   ```bash
   cd backend
   python app.py
   ```
   
   **Windows:**
   ```cmd
   cd backend
   python app.py
   ```

6. **Open Your Browser**
   Navigate to `http://localhost:8000` and start learning! 🎉

> 💡 **Tip:** Use the automated setup scripts in the `deployment/` folder for a one-click installation experience!

## 🔧 Troubleshooting

### Common Issues

**Python not found:**
- **Windows:** Make sure Python is installed and added to PATH. Try `py app.py` instead of `python app.py`
- **Linux:** Install Python with `sudo apt install python3 python3-pip` (Ubuntu/Debian)

**Permission denied (Linux):**
```bash
sudo chmod +x backend/app.py
```

**npm not found:**
- **Windows:** Download Node.js from [nodejs.org](https://nodejs.org)
- **Linux:** Install with `sudo apt install nodejs npm` (Ubuntu/Debian)

**Port already in use:**
- Kill existing processes on port 8000 or change port in `app.py`

## 🏗️ Project Structure

```
CyberQuestJR/
├── backend/
│   ├── app.py              # FastAPI server
│   ├── static/             # Built frontend files
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # Theme context
│   │   └── services/       # API calls
│   ├── package.json        # Node dependencies
│   └── tailwind.config.js  # Styling config
└── README.md
```

## 🎯 Learning Topics

- **Password Security** - Creating strong passwords
- **Social Engineering** - Recognizing online tricks
- **Email Safety** - Identifying phishing attempts
- **Network Security** - Understanding Wi-Fi safety
- **Digital Footprints** - Managing online presence

## 🔧 Configuration

### Optional: OpenAI Integration
Create a `.env` file in the backend directory:

**Linux/macOS:**
```bash
cd backend
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

**Windows:**
```cmd
cd backend
echo OPENAI_API_KEY=your_api_key_here > .env
```

Or manually create the file with any text editor:
```
OPENAI_API_KEY=your_api_key_here
```

Without OpenAI, the app uses built-in educational content.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built with React, TypeScript, and Tailwind CSS
- Backend powered by FastAPI and SQLAlchemy
- Icons from Lucide React
- Created for young cybersecurity enthusiasts! 🚀

---

**Made with ❤️ for digital safety education**
