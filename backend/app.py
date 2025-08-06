from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyberquest.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    openai.api_key = openai_api_key
    OPENAI_ENABLED = True
    print("✅ OpenAI API enabled")
else:
    OPENAI_ENABLED = False
    print("⚠️  OpenAI API key not found - using fallback content")

app = FastAPI(title="CyberQuest Jr", description="Cybersecurity Education Platform for Kids", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class QuizProgress(Base):
    __tablename__ = "quiz_progress"
    id = Column(Integer, primary_key=True, index=True)
    quiz_type = Column(String, index=True)
    score = Column(Float)
    completed_at = Column(DateTime, default=datetime.utcnow)
    level = Column(String)

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"
    id = Column(Integer, primary_key=True, index=True)
    anonymous_name = Column(String, index=True)
    total_score = Column(Float)
    quizzes_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class QuizResult(BaseModel):
    score: float
    level: str
    feedback: dict

class QuizSubmission(BaseModel):
    quiz_type: str
    answers: List[dict]
    anonymous_name: Optional[str] = "Young Hero"

class ProgressUpdate(BaseModel):
    module_name: str
    progress: float

FALLBACK_QUIZZES = {
    "password": {
        "title": "Password Security Basics 🔐",
        "questions": [
            {
                "id": 1,
                "question": "What makes a password strong?",
                "options": ["Using only letters", "Making it at least 8 characters with mixed case, numbers, and symbols", "Using your birthday", "Using the same password everywhere"],
                "correct_answer": "Making it at least 8 characters with mixed case, numbers, and symbols",
                "explanation": "Strong passwords are long and use a mix of different character types! 💪"
            },
            {
                "id": 2,
                "question": "Should you share your password with friends?",
                "options": ["Yes, with best friends only", "No, never share passwords", "Only for games", "Only with family"],
                "correct_answer": "No, never share passwords",
                "explanation": "Passwords are like toothbrushes - they're personal and shouldn't be shared! 🦷"
            },
            {
                "id": 3,
                "question": "What should you do if you forget your password?",
                "options": ["Ask friends to guess it", "Use the 'forgot password' feature", "Create a new account", "Give up using the service"],
                "correct_answer": "Use the 'forgot password' feature",
                "explanation": "Most websites have safe ways to reset your password when you forget it! 🔄"
            }
        ]
    },
    "phishing": {
        "title": "Spot the Phishing 🎣",
        "questions": [
            {
                "id": 1,
                "question": "What is phishing?",
                "options": ["A type of fishing sport", "Tricking people to give away personal information", "A computer game", "A type of virus"],
                "correct_answer": "Tricking people to give away personal information",
                "explanation": "Phishing is when bad people pretend to be someone you trust to steal your information! 🎭"
            },
            {
                "id": 2,
                "question": "How can you spot a phishing email?",
                "options": ["It asks for passwords or personal info", "It has spelling mistakes", "It creates urgency", "All of the above"],
                "correct_answer": "All of the above",
                "explanation": "Great job! Phishing emails often have all these red flags! 🚩"
            },
            {
                "id": 3,
                "question": "What should you do if you receive a suspicious email?",
                "options": ["Click all the links", "Forward it to friends", "Delete it and tell an adult", "Reply with your information"],
                "correct_answer": "Delete it and tell an adult",
                "explanation": "When in doubt, delete and tell a trusted adult! They can help keep you safe! 👨‍👩‍👧‍👦"
            }
        ]
    },
    "social": {
        "title": "Social Media Safety 📱",
        "questions": [
            {
                "id": 1,
                "question": "What information should you NEVER share online?",
                "options": ["Your favorite color", "Your home address", "Your favorite food", "Your hobby"],
                "correct_answer": "Your home address",
                "explanation": "Personal information like your address should stay private! 🏠🔒"
            },
            {
                "id": 2,
                "question": "Who should you accept friend requests from?",
                "options": ["Anyone who asks", "Only people you know in real life", "People with cool profile pictures", "Everyone in your school"],
                "correct_answer": "Only people you know in real life",
                "explanation": "Only add people you actually know and trust! 👥✅"
            },
            {
                "id": 3,
                "question": "What should you do if someone online makes you uncomfortable?",
                "options": ["Tell them to stop and inform an adult", "Ignore it", "Argue with them", "Block them without telling anyone"],
                "correct_answer": "Tell them to stop and inform an adult",
                "explanation": "Always speak up and get help from a trusted adult when something doesn't feel right! 🗣️"
            }
        ]
    }
}

LEARNING_MODULES = {
    "password-basics": {
        "title": "Password Power! 🔐",
        "description": "Learn how to create super-strong passwords that keep your accounts safe!",
        "content": {
            "sections": [
                {
                    "title": "What are Passwords? 🤔",
                    "content": "Passwords are like secret keys that protect your online accounts. Just like you wouldn't give your house key to a stranger, you should keep your passwords safe and secret!"
                },
                {
                    "title": "Making Strong Passwords 💪",
                    "content": "Strong passwords are like strong shields! They should be:\n• At least 8 characters long\n• Mix of uppercase and lowercase letters\n• Include numbers and symbols\n• Not use personal information (like your name or birthday)"
                },
                {
                    "title": "Password Tips 💡",
                    "content": "Here are some super tips:\n• Use different passwords for different accounts\n• Think of a fun sentence and use the first letters\n• Never share your passwords with friends\n• Ask a parent to help you use a password manager"
                }
            ]
        }
    },
    "phishing-awareness": {
        "title": "Phishing Detectives 🕵️",
        "description": "Become a phishing detective and learn to spot fake emails and websites!",
        "content": {
            "sections": [
                {
                    "title": "What is Phishing? 🎣",
                    "content": "Phishing is when bad people pretend to be someone you trust (like your bank or a game company) to trick you into giving them your personal information. It's like fishing, but instead of fish, they're trying to catch your secrets!"
                },
                {
                    "title": "Spotting Phishing Emails 👀",
                    "content": "Look out for these warning signs:\n• Spelling and grammar mistakes\n• Urgent messages like 'Act now!'\n• Asking for passwords or personal info\n• Sender's email looks suspicious\n• Links that don't match the real website"
                },
                {
                    "title": "Stay Safe! 🛡️",
                    "content": "If you get a suspicious email:\n• Don't click any links\n• Don't download attachments\n• Delete the email\n• Tell a trusted adult\n• When in doubt, check with the real company directly"
                }
            ]
        }
    },
    "social-media-safety": {
        "title": "Social Media Superhero 📱",
        "description": "Learn how to have fun on social media while staying safe and protecting your privacy!",
        "content": {
            "sections": [
                {
                    "title": "Privacy Settings are Your Superpower! ⚙️",
                    "content": "Privacy settings help you control who can see your posts and information. Always set your accounts to private and only accept friend requests from people you know in real life!"
                },
                {
                    "title": "What NOT to Share 🚫",
                    "content": "Never share these online:\n• Your full name, address, or phone number\n• Your school name or location\n• Photos that show where you live\n• Your daily schedule or plans\n• Passwords or personal family information"
                },
                {
                    "title": "Dealing with Cyberbullies 🛡️",
                    "content": "If someone is mean to you online:\n• Don't respond to mean messages\n• Block and report the person\n• Save evidence (screenshots)\n• Tell a trusted adult immediately\n• Remember: it's not your fault!"
                }
            ]
        }
    }
}

@app.get("/api/quiz/generate/{quiz_type}")
async def generate_quiz(quiz_type: str):
    """Generate a cybersecurity quiz - no authentication needed!"""
    
    if quiz_type not in FALLBACK_QUIZZES:
        raise HTTPException(status_code=404, detail="Quiz type not found.")
    
    if OPENAI_ENABLED:
        try:
            prompt = f"""Create a fun, educational cybersecurity quiz about {quiz_type} for children aged 8-18. 
            Make it engaging with emojis and age-appropriate language.
            
            Return ONLY a JSON object with this structure:
            {{
                "title": "Quiz Title",
                "questions": [
                    {{
                        "id": 1,
                        "question": "Question text",
                        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                        "correct_answer": "Correct option text",
                        "explanation": "Kid-friendly explanation with emoji"
                    }}
                ]
            }}
            
            Create 3-5 questions. Make sure explanations are encouraging and educational."""
            
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            quiz_data = json.loads(response.choices[0].message.content)
            return quiz_data
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
    
    return FALLBACK_QUIZZES[quiz_type]

@app.post("/api/quiz/submit")
async def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    """Submit quiz answers and get results - no authentication needed!"""
    
    total_questions = len(submission.answers)
    correct_answers = sum(1 for answer in submission.answers if answer.get("is_correct", False))
    score = (correct_answers / total_questions) * 100
    
    if score >= 80:
        level = "Expert! 🏆"
        feedback = {
            "title": "Amazing Work! 🌟",
            "message": "You're a cybersecurity superstar!",
            "encouragement": "Keep up the fantastic work! 🚀"
        }
    elif score >= 60:
        level = "Good Job! 👍"
        feedback = {
            "title": "Well Done! 😊",
            "message": "You're learning fast!",
            "encouragement": "Practice makes perfect! 💪"
        }
    else:
        level = "Keep Learning! 📚"
        feedback = {
            "title": "Great Start! 🌱",
            "message": "Every expert was once a beginner!",
            "encouragement": "Don't give up - you've got this! 🎯"
        }
    
    # Save progress to database
    progress = QuizProgress(
        quiz_type=submission.quiz_type,
        score=score,
        level=level
    )
    db.add(progress)
    
    # Update leaderboard
    leaderboard_entry = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.anonymous_name == submission.anonymous_name
    ).first()
    
    if leaderboard_entry:
        leaderboard_entry.total_score += score
        leaderboard_entry.quizzes_completed += 1
    else:
        leaderboard_entry = LeaderboardEntry(
            anonymous_name=submission.anonymous_name,
            total_score=score,
            quizzes_completed=1
        )
        db.add(leaderboard_entry)
    
    db.commit()
    
    return QuizResult(score=score, level=level, feedback=feedback)

@app.get("/api/modules/{module_name}")
async def get_module(module_name: str):
    """Get learning module content - no authentication needed!"""
    
    if module_name not in LEARNING_MODULES:
        raise HTTPException(status_code=404, detail="Module not found.")
    
    return LEARNING_MODULES[module_name]

@app.get("/api/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    """Get the leaderboard - no authentication needed!"""
    
    entries = db.query(LeaderboardEntry).order_by(
        LeaderboardEntry.total_score.desc()
    ).limit(10).all()
    
    return [
        {
            "rank": idx + 1,
            "name": entry.anonymous_name,
            "score": round(entry.total_score, 1),
            "quizzes_completed": entry.quizzes_completed
        }
        for idx, entry in enumerate(entries)
    ]

@app.get("/api/progress")
async def get_progress():
    """Get general progress stats - no authentication needed!"""
    
    return {
        "available_modules": len(LEARNING_MODULES),
        "available_quizzes": len(FALLBACK_QUIZZES),
        "message": "Start learning anytime - no account needed! 🎉"
    }

app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

@app.get("/{path:path}")
async def serve_frontend_routes(path: str):
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    print("🛡️  Starting CyberQuest Jr on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
