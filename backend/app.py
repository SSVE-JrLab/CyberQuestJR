from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import re
import random
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cyberquest.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    experience_level = Column(String)
    interests = Column(Text)  # JSON string of interests
    created_at = Column(DateTime, default=datetime.utcnow)

class CourseProgress(Base):
    __tablename__ = "course_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    course_id = Column(String, index=True)
    completed = Column(Boolean, default=False)
    score = Column(Float, default=0.0)
    completion_date = Column(DateTime, nullable=True)
    course_content = Column(Text)  # AI-generated course content
    quiz_attempts = Column(Integer, default=0)
    best_quiz_score = Column(Float, default=0.0)

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    issued_date = Column(DateTime, default=datetime.utcnow)
    certificate_id = Column(String, unique=True, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class UserCreate(BaseModel):
    name: str
    age: int
    experience_level: str
    interests: List[str]

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    experience_level: str
    interests: List[str]

class CourseRequest(BaseModel):
    user_id: int
    course_id: str

class QuizAnswer(BaseModel):
    user_id: int
    course_id: str
    answers: Dict[str, Any]

class CourseContent(BaseModel):
    content: str
    exercises: List[Dict[str, Any]]
    quiz: Dict[str, Any]

# Course definitions
COURSES = {
    "password-basics": {
        "title": "Password Heroes",
        "description": "Learn to create super strong passwords that protect your digital world like a superhero shield!",
        "icon": "🔐",
        "level": "Beginner",
        "difficulty": 1,
        "estimatedTime": "15 min"
    },
    "phishing-awareness": {
        "title": "Phishing Detective",
        "description": "Become an expert detective at spotting fake emails and suspicious messages that try to trick you!",
        "icon": "🕵️",
        "level": "Beginner",
        "difficulty": 1,
        "estimatedTime": "20 min"
    },
    "digital-footprints": {
        "title": "Digital Footprint Tracker",
        "description": "Understand what traces you leave online and how to manage them like a pro!",
        "icon": "👣",
        "level": "Intermediate",
        "difficulty": 2,
        "estimatedTime": "25 min"
    },
    "social-media-safety": {
        "title": "Safe Social Media",
        "description": "Navigate social platforms safely and responsibly while having fun with friends!",
        "icon": "📱",
        "level": "Intermediate",
        "difficulty": 2,
        "estimatedTime": "30 min"
    },
    "cyber-bullying": {
        "title": "Cyber Bullying Defense",
        "description": "Learn to identify, prevent, and respond to online bullying like a true cyber warrior!",
        "icon": "🛡️",
        "level": "Intermediate",
        "difficulty": 2,
        "estimatedTime": "25 min"
    },
    "privacy-guardian": {
        "title": "Privacy Guardian",
        "description": "Master the art of protecting your personal information and privacy online!",
        "icon": "🔒",
        "level": "Advanced",
        "difficulty": 3,
        "estimatedTime": "35 min"
    }
}

# FastAPI app
app = FastAPI(title="CyberQuest Jr", description="AI-Powered Cybersecurity Education Platform")

# Mount static files FIRST to ensure they take priority over route handlers
if os.path.exists("static"):
    # Mount assets at root level for proper frontend serving
    if os.path.exists("static/assets"):
        app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    # Mount static directory for other files
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
    print("🤖 Google Gemini AI initialized successfully!")
else:
    gemini_model = None
    print("⚠️ Warning: GEMINI_API_KEY not found. AI features will use fallback content.")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility functions
def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength with detailed feedback"""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 2
    else:
        feedback.append("Password should be at least 8 characters long")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Include at least one uppercase letter")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Include at least one lowercase letter")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include at least one number")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Include at least one special character")

    strength = "Weak"
    if score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Medium"

    return {
        "score": score,
        "max_score": 6,
        "strength": strength,
        "feedback": feedback,
        "is_strong": score >= 5
    }

def validate_email_safety(email: str) -> Dict[str, Any]:
    """Check if an email looks suspicious"""
    suspicious_domains = ["fakeemail.com", "phishing.net", "suspicious.org", "scam.biz"]
    suspicious_keywords = ["urgent", "winner", "prize", "click now", "verify account", "suspended"]

    is_suspicious = False
    warnings = []

    # Check domain
    if "@" in email:
        domain = email.split("@")[1].lower()
        if domain in suspicious_domains:
            is_suspicious = True
            warnings.append(f"Domain '{domain}' is known to be suspicious")

    # Check for suspicious keywords
    email_lower = email.lower()
    for keyword in suspicious_keywords:
        if keyword in email_lower:
            is_suspicious = True
            warnings.append(f"Contains suspicious keyword: '{keyword}'")

    return {
        "is_suspicious": is_suspicious,
        "warnings": warnings,
        "safety_score": 0 if is_suspicious else 100
    }

def generate_certificate_id() -> str:
    """Generate a unique certificate ID"""
    import uuid
    return f"CQ-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

# API Routes

@app.post("/api/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user profile"""
    db_user = User(
        name=user.name,
        age=user.age,
        experience_level=user.experience_level,
        interests=",".join(user.interests)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        name=db_user.name,
        age=db_user.age,
        experience_level=db_user.experience_level,
        interests=db_user.interests.split(",") if db_user.interests else []
    )

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        name=user.name,
        age=user.age,
        experience_level=user.experience_level,
        interests=user.interests.split(",") if user.interests else []
    )

@app.get("/api/courses")
async def get_courses():
    """Get all available courses"""
    return {"courses": COURSES}

@app.post("/api/courses/generate")
async def generate_course_content(request: CourseRequest, db: Session = Depends(get_db)):
    """Generate AI-powered course content"""
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.course_id not in COURSES:
        raise HTTPException(status_code=404, detail="Course not found")

    course_info = COURSES[request.course_id]

    # Check if content already exists
    existing_progress = db.query(CourseProgress).filter(
        CourseProgress.user_id == request.user_id,
        CourseProgress.course_id == request.course_id
    ).first()

    if existing_progress and existing_progress.course_content:
        # Return existing content
        import json
        return json.loads(existing_progress.course_content)

    # Generate new content using AI
    try:
        user_interests = user.interests.split(",") if user.interests else []

        prompt = f"""
        Create educational content for a cybersecurity course for children aged {user.age}.

        Course: {course_info['title']} - {course_info['description']}
        User Experience Level: {user.experience_level}
        User Interests: {', '.join(user_interests)}

        Generate a comprehensive course with:
        1. Educational content (explanation, examples, tips) - make it engaging and age-appropriate
        2. 3 practical exercises with clear instructions
        3. A quiz with 5 multiple-choice questions

        Format the response as JSON with this structure:
        {{
            "content": "detailed educational content here",
            "exercises": [
                {{
                    "title": "exercise title",
                    "description": "what to do",
                    "type": "password|email|scenario",
                    "instructions": "step by step instructions"
                }}
            ],
            "quiz": {{
                "questions": [
                    {{
                        "question": "question text",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": 0,
                        "explanation": "why this is correct"
                    }}
                ]
            }}
        }}

        Make it fun, educational, and appropriate for a {user.age}-year-old with {user.experience_level} experience.
        """

        if gemini_model:
            response = gemini_model.generate_content(prompt)
        else:
            # Fallback if AI is not available
            response = type('obj', (object,), {'text': '{"content": "Course content not available", "exercises": [], "quiz": {"questions": []}}'})

        response_text = response.text if hasattr(response, 'text') else str(response)

        # Parse AI response
        import json
        try:
            course_content = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback content if AI response isn't valid JSON
            course_content = {
                "content": f"Welcome to {course_info['title']}! This course will teach you about {course_info['description'].lower()}.",
                "exercises": [
                    {
                        "title": "Basic Understanding",
                        "description": "Complete this exercise to test your understanding",
                        "type": "scenario",
                        "instructions": "Read the scenario and choose the best response"
                    }
                ],
                "quiz": {
                    "questions": [
                        {
                            "question": f"What is the main goal of {course_info['title']}?",
                            "options": ["To have fun", "To learn cybersecurity", "To use computers", "To play games"],
                            "correct_answer": 1,
                            "explanation": "The main goal is to learn cybersecurity concepts"
                        }
                    ]
                }
            }

        # Save content to database
        if existing_progress:
            existing_progress.course_content = json.dumps(course_content)
        else:
            progress = CourseProgress(
                user_id=request.user_id,
                course_id=request.course_id,
                course_content=json.dumps(course_content)
            )
            db.add(progress)

        db.commit()

        return course_content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate course content: {str(e)}")

@app.post("/api/courses/submit-quiz")
async def submit_quiz(answer: QuizAnswer, db: Session = Depends(get_db)):
    """Submit quiz answers and get results"""
    user = db.query(User).filter(User.id == answer.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    progress = db.query(CourseProgress).filter(
        CourseProgress.user_id == answer.user_id,
        CourseProgress.course_id == answer.course_id
    ).first()

    if not progress or not progress.course_content:
        raise HTTPException(status_code=404, detail="Course content not found")

    import json
    course_content = json.loads(progress.course_content)
    quiz = course_content.get("quiz", {})
    questions = quiz.get("questions", [])

    # Calculate score
    correct_answers = 0
    total_questions = len(questions)
    results = []

    for i, question in enumerate(questions):
        user_answer = answer.answers.get(str(i), -1)
        correct_answer = question.get("correct_answer", -1)
        is_correct = user_answer == correct_answer

        if is_correct:
            correct_answers += 1

        results.append({
            "question": question.get("question", ""),
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question.get("explanation", "")
        })

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    passed = score >= 70  # 70% passing grade

    # Update progress
    progress.quiz_attempts += 1
    if score > progress.best_quiz_score:
        progress.best_quiz_score = score

    if passed and not progress.completed:
        progress.completed = True
        progress.completion_date = datetime.utcnow()
        progress.score = score

    db.commit()

    return {
        "score": score,
        "passed": passed,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "results": results,
        "attempts": progress.quiz_attempts
    }

@app.post("/api/exercises/validate")
async def validate_exercise(data: Dict[str, Any]):
    """Validate exercise answers"""
    exercise_type = data.get("type", "")
    answer = data.get("answer", "")

    if exercise_type == "password":
        return validate_password_strength(answer)
    elif exercise_type == "email":
        return validate_email_safety(answer)
    elif exercise_type == "scenario":
        # For scenario-based exercises, provide feedback
        return {
            "feedback": "Good thinking! Remember to always verify suspicious messages.",
            "score": 85,
            "tips": ["Always check the sender", "Look for spelling mistakes", "Verify links before clicking"]
        }
    else:
        return {"error": "Unknown exercise type"}

@app.get("/api/users/{user_id}/progress")
async def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    """Get user's progress across all courses"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    progress_records = db.query(CourseProgress).filter(CourseProgress.user_id == user_id).all()

    progress = {}
    completed_courses = 0
    total_score = 0

    for record in progress_records:
        progress[record.course_id] = {
            "completed": record.completed,
            "score": record.score,
            "completion_date": record.completion_date.isoformat() if record.completion_date else None,
            "quiz_attempts": record.quiz_attempts,
            "best_quiz_score": record.best_quiz_score
        }

        if record.completed:
            completed_courses += 1
            total_score += record.score

    # Check if eligible for certificate
    eligible_for_certificate = completed_courses == len(COURSES)

    # Check if certificate already issued
    certificate = None
    if eligible_for_certificate:
        cert_record = db.query(Certificate).filter(Certificate.user_id == user_id).first()
        if cert_record:
            certificate = {
                "certificate_id": cert_record.certificate_id,
                "issued_date": cert_record.issued_date.isoformat()
            }

    return {
        "user_id": user_id,
        "completed_courses": completed_courses,
        "total_courses": len(COURSES),
        "average_score": total_score / completed_courses if completed_courses > 0 else 0,
        "progress": progress,
        "eligible_for_certificate": eligible_for_certificate,
        "certificate": certificate
    }

@app.post("/api/users/{user_id}/certificate")
async def issue_certificate(user_id: int, db: Session = Depends(get_db)):
    """Issue a certificate to a user who completed all courses"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user completed all courses
    completed_courses = db.query(CourseProgress).filter(
        CourseProgress.user_id == user_id,
        CourseProgress.completed == True
    ).count()

    if completed_courses != len(COURSES):
        raise HTTPException(status_code=400, detail="User must complete all courses to receive certificate")

    # Check if certificate already exists
    existing_cert = db.query(Certificate).filter(Certificate.user_id == user_id).first()
    if existing_cert:
        return {
            "certificate_id": existing_cert.certificate_id,
            "issued_date": existing_cert.issued_date.isoformat(),
            "message": "Certificate already issued"
        }

    # Issue new certificate
    certificate_id = generate_certificate_id()
    certificate = Certificate(
        user_id=user_id,
        certificate_id=certificate_id
    )

    db.add(certificate)
    db.commit()

    return {
        "certificate_id": certificate_id,
        "issued_date": certificate.issued_date.isoformat(),
        "message": "Congratulations! You've completed all CyberQuest Jr courses!"
    }

@app.get("/api/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    """Get leaderboard of top performers"""
    # Get users with their progress
    users = db.query(User).all()
    leaderboard = []

    for user in users:
        progress_records = db.query(CourseProgress).filter(
            CourseProgress.user_id == user.id,
            CourseProgress.completed == True
        ).all()

        if progress_records:
            total_score = sum(record.score for record in progress_records)
            avg_score = total_score / len(progress_records)
            completed_courses = len(progress_records)

            # Check for certificate
            has_certificate = db.query(Certificate).filter(Certificate.user_id == user.id).first() is not None

            leaderboard.append({
                "name": user.name,
                "completed_courses": completed_courses,
                "average_score": round(avg_score, 1),
                "total_score": round(total_score, 1),
                "has_certificate": has_certificate
            })

    # Sort by completed courses, then by average score
    leaderboard.sort(key=lambda x: (x["completed_courses"], x["average_score"]), reverse=True)

    return {"leaderboard": leaderboard[:10]}  # Top 10

# Move static file mounting to the end, after all API routes are defined
# This will be moved after all route definitions

@app.get("/")
async def read_root():
    """Serve the frontend application"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return {"message": "CyberQuest Jr API is running! Please build the frontend first."}

@app.get("/favicon.ico")
@app.get("/shield.svg")
async def serve_favicon():
    """Serve favicon - return 404 if not found"""
    raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/{path:path}")
async def serve_spa(path: str):
    """Serve the SPA for any route (React Router support) - but not for assets"""
    # Don't serve SPA for asset requests
    if path.startswith("assets/") or path.startswith("static/"):
        raise HTTPException(status_code=404, detail="Asset not found")

    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return {"message": "Frontend not found. Please build the frontend first."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
