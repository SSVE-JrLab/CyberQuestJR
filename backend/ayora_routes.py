"""
Ayora AI Companion API endpoints for dynamic voice and animation integration
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sys
import os
import subprocess
import json

# Add the AI directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ai"))

try:
    from ayora_voice import ayora_voice, AyoraContext, generate_landing_introduction, generate_contextual_speech
    AYORA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Ayora voice engine not available: {e}")
    AYORA_AVAILABLE = False

router = APIRouter(prefix="/api/ayora", tags=["Ayora AI Companion"])

class AyoraRequest(BaseModel):
    context: str
    context_data: Optional[Dict[str, Any]] = None
    trigger_animations: bool = True

class AyoraSpeechResponse(BaseModel):
    success: bool
    speech_text: str
    animation_sequence: list
    companion_name: str
    context: str
    estimated_duration: float
    audio_filename: Optional[str] = None
    error: Optional[str] = None

@router.post("/landing-introduction", response_model=AyoraSpeechResponse)
async def get_landing_introduction():
    """Generate Ayora's landing page introduction with speech and animation sequence"""
    
    if not AYORA_AVAILABLE:
        return AyoraSpeechResponse(
            success=False,
            speech_text="",
            animation_sequence=[],
            companion_name="Ayora",
            context="landing_introduction",
            estimated_duration=0.0,
            error="Ayora voice engine not available"
        )
    
    try:
        # Generate landing introduction
        result = await generate_landing_introduction()
        
        return AyoraSpeechResponse(
            success=result.get("success", False),
            speech_text=result.get("speech_text", ""),
            animation_sequence=result.get("animation_sequence", []),
            companion_name=result.get("companion_name", "Ayora"),
            context=result.get("context", "landing_introduction"),
            estimated_duration=result.get("estimated_duration", 0.0),
            audio_filename=result.get("audio_filename"),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate landing introduction: {str(e)}")

@router.post("/contextual-speech", response_model=AyoraSpeechResponse)
async def generate_contextual_speech(request: AyoraRequest):
    """Generate contextual speech based on user's current activity"""
    
    if not AYORA_AVAILABLE:
        return AyoraSpeechResponse(
            success=False,
            speech_text="",
            animation_sequence=[],
            companion_name="Ayora",
            context=request.context,
            estimated_duration=0.0,
            error="Ayora voice engine not available"
        )
    
    try:
        # Convert string context to enum
        context_map = {
            "landing_introduction": AyoraContext.LANDING_INTRODUCTION,
            "module_explanation": AyoraContext.MODULE_EXPLANATION,
            "quiz_encouragement": AyoraContext.QUIZ_ENCOURAGEMENT,
            "achievement_celebration": AyoraContext.ACHIEVEMENT_CELEBRATION,
            "help_guidance": AyoraContext.HELP_GUIDANCE
        }
        
        context_enum = context_map.get(request.context)
        if not context_enum:
            raise HTTPException(status_code=400, detail=f"Invalid context: {request.context}")
        
        # Generate contextual speech
        result = await generate_contextual_speech(
            context=request.context,
            context_data=request.context_data
        )
        
        return AyoraSpeechResponse(
            success=result.get("success", False),
            speech_text=result.get("speech_text", ""),
            animation_sequence=result.get("animation_sequence", []),
            companion_name=result.get("companion_name", "Ayora"),
            context=result.get("context", request.context),
            estimated_duration=result.get("estimated_duration", 0.0),
            audio_filename=result.get("audio_filename"),
            error=result.get("error")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate contextual speech: {str(e)}")

@router.get("/animation-config")
async def get_animation_config():
    """Get animation configuration for frontend integration"""
    
    if not AYORA_AVAILABLE:
        return {
            "available": False,
            "error": "Ayora voice engine not available"
        }
    
    try:
        if hasattr(ayora_voice, 'animation_config'):
            config = {
                "available": True,
                "waving_duration": 3.0,
                "talking_buffer": 0.5,
                "available_animations": ["breathing_idle", "waving", "talking"],
                "companion_name": "Ayora",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.8,
                    "style": 0.8,
                    "speed": 1.1
                }
            }
        else:
            config = {
                "available": True,
                "waving_duration": 3.0,
                "talking_buffer": 0.5,
                "available_animations": ["breathing_idle", "waving", "talking"],
                "companion_name": "Ayora"
            }
        
        return config
        
    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }

@router.get("/status")
async def get_ayora_status():
    """Get current status of Ayora AI companion system"""
    
    status = {
        "ayora_available": AYORA_AVAILABLE,
        "speech_generator_available": False,
        "tts_available": False,
        "openai_available": False,
        "elevenlabs_available": False
    }
    
    if AYORA_AVAILABLE:
        try:
            # Check speech generator
            if hasattr(ayora_voice, 'speech_generator'):
                status["speech_generator_available"] = True
            
            # Check TTS
            if hasattr(ayora_voice, 'tts_enabled'):
                status["tts_available"] = ayora_voice.tts_enabled
            
            # Check OpenAI (indirectly through speech generator)
            try:
                import openai
                status["openai_available"] = bool(openai.api_key)
            except:
                status["openai_available"] = False
            
            # Check ElevenLabs
            try:
                status["elevenlabs_available"] = bool(os.getenv("ELEVENLABS_API_KEY"))
            except:
                status["elevenlabs_available"] = False
                
        except Exception as e:
            status["error"] = str(e)
    
    return status

@router.post("/test-landing")
async def test_landing_introduction():
    """Test endpoint for Ayora landing introduction"""
    
    try:
        # Run the text-to-speech script directly for testing
        script_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "app", "text_to_speech.py")
        
        if os.path.exists(script_path):
            result = subprocess.run(
                ["python", script_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "message": "Landing introduction test completed"
            }
        else:
            return {
                "success": False,
                "error": "Text-to-speech script not found",
                "script_path": script_path
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Test timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
