# 🛡️ CyberQuest Jr

**An AI-powered cybersecurity education platform for kids aged 8-18!**

## ✨ Features

- 🤖 **AI-Powered Learning** - Personalized cybersecurity education with Google Gemini AI
- 🎯 **Adaptive Assessment** - Smart quizzes that adapt to your skill level
- 📚 **Dynamic Course Generation** - AI creates custom learning paths based on your performance
- 🎮 **Interactive Gaming Modules** - 6 engaging cybersecurity challenges and scenarios
- 📊 **Progress Tracking** - Monitor learning journey with XP, levels, and achievements
- 🎨 **Modern UI** - Beautiful, kid-friendly interface with dark/light mode
- 🔐 **No Authentication Required** - Jump right in and start learning!

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Linux/macOS:**

```bash
git clone https://github.com/Aarav2709/CyberQuestJR.git
cd CyberQuestJR
chmod +x deployment/linux.sh
./deployment/linux.sh
./start.sh
```

**Windows:**

1. Clone or download the repository
2. Double-click `deployment/windows.bat`
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
   pip install -r requirements.txt
   ```

   **Windows:**

   ```cmd
   cd backend
   pip install -r requirements.txt
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
   mkdir -p backend/static
   cp -r frontend/dist/* backend/static/
   ```

   **Windows:**

   ```cmd
   cd ..
   mkdir backend\static
   xcopy frontend\dist backend\static /E /I /Y
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
│   ├── app.py              # Unified FastAPI server
│   ├── api/
│   │   └── routes.py       # API endpoints
│   ├── ai/
│   │   └── challenge_generator.py  # AI content generation
│   ├── database/
│   │   ├── models.py       # Database models
│   │   └── database.py     # Database setup
│   ├── static/             # Built frontend files
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # Application contexts
│   │   └── services/       # API integration
│   ├── package.json        # Node dependencies
│   └── tailwind.config.js  # Styling config
├── deployment/
│   ├── setup-linux.sh      # Linux setup script
│   └── setup-windows.bat   # Windows setup script
└── README.md
```

## 🎯 Learning Modules

1. **Password Heroes** 🔐 - Learn to create super-strong passwords
2. **Phishing Detective** 🕵️ - Spot fake emails and websites
3. **Digital Footprints** 👣 - Understand your online traces
4. **Social Media Safety** 📱 - Safe sharing and privacy
5. **Cyber Bullying Defense** 🛡️ - Handle online bullying
6. **Privacy Guardian** 🔒 - Protect personal information

Each module uses AI to generate personalized challenges based on your skill level!

## 🔧 Configuration

### Required: Google Gemini AI Integration

Create a `.env` file in the backend directory:

**Linux/macOS:**

```bash
cd backend
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

**Windows:**

```cmd
cd backend
echo GEMINI_API_KEY=your_gemini_api_key_here > .env
```

Or manually create the file with any text editor:

```
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./cyberquest_game.db
```

**Get your Google Gemini API key:**

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy your API key to the `.env` file

The AI features require a valid Google Gemini API key for personalized content generation.

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
- AI content generation by Google Gemini
- Icons from Lucide React
- Created for young cybersecurity enthusiasts! 🚀

## 🔮 AI-Powered Features

- **Adaptive Learning:** AI analyzes performance and adjusts difficulty
- **Personalized Courses:** Custom learning paths generated based on your strengths/weaknesses
- **Dynamic Content:** Fresh challenges and scenarios created in real-time
- **Smart Assessment:** Intelligent skill evaluation and gap identification
- **Contextual Hints:** AI provides personalized guidance when you're stuck

---

**Made with ❤️ for digital safety education**
