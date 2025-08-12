"""
Ayora Voice Engine - AI Companion Voice and Animation System
Integrates OpenAI for speech generation and ElevenLabs for TTS
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, Optional, List
from enum import Enum
from pathlib import Path

# Add the frontend app directory to path
frontend_app_path = Path(__file__).parent.parent.parent / "frontend" / "app"
sys.path.append(str(frontend_app_path))

try:
    import openai
    from elevenlabs import VoiceSettings, ElevenLabs
    from elevenlabs import stream as play_stream
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Missing dependencies for Ayora voice engine: {e}")
    DEPENDENCIES_AVAILABLE = False

class AyoraContext(Enum):
    LANDING_INTRODUCTION = "landing_introduction"
    MODULE_EXPLANATION = "module_explanation"
    QUIZ_ENCOURAGEMENT = "quiz_encouragement"
    ACHIEVEMENT_CELEBRATION = "achievement_celebration"
    HELP_GUIDANCE = "help_guidance"

class AnimationState(Enum):
    BREATHING_IDLE = "Breathing Idle"
    WAVING = "Waving (1)"
    TALKING = "Talking (1)"

class AyoraVoiceEngine:
    def __init__(self):
        """Initialize Ayora Voice Engine with OpenAI and ElevenLabs"""
        self.companion_name = "Ayora"
        
        if not DEPENDENCIES_AVAILABLE:
            print("❌ Ayora Voice Engine: Dependencies not available")
            return
            
        # OpenAI Configuration
        try:
            from openai import OpenAI
            self.openai_api_key = os.getenv("OPENAI_API_KEY", "KEYHERE")
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        except ImportError:
            print("OpenAI package not available")
            self.openai_client = None
        
        # ElevenLabs Configuration
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if self.elevenlabs_api_key:
            self.elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
            self.voice_id = "Xb7hH8MSUJpSbSDYk0k2"  # Female voice ID
            self.voice_settings = VoiceSettings(
                stability=0.3,
                similarity_boost=0.75,
                style=1.0,
                speed=1.2
            )
        else:
            print("⚠️  ElevenLabs API key not found - TTS disabled")
            self.elevenlabs_client = None
        
        # Animation timing configuration
        self.animation_config = {
            "waving_duration": 3.0,
            "talking_buffer": 0.5,
        }
        
        print(f"🤖 {self.companion_name} Voice Engine initialized!")

    def generate_speech_text(self, context: AyoraContext, context_data: Optional[Dict] = None) -> str:
        """Generate speech text using OpenAI based on context"""
        
        if not DEPENDENCIES_AVAILABLE:
            return "Hello! I'm Ayora, your cybersecurity companion!"
        
        prompts = {
            AyoraContext.LANDING_INTRODUCTION: """
                You are Ayora, a friendly and enthusiastic AI companion for CyberQuestJR, a cybersecurity education platform for kids aged 8-18.

                Generate a warm, welcoming introduction for when a user first lands on the website. Include:
                - Introduce yourself as Ayora, their personal cybersecurity guide
                - Welcome them to CyberQuestJR in an exciting, kid-friendly way
                - Briefly explain that you'll be helping them throughout their cybersecurity learning journey
                - Mention that they'll learn to protect themselves online through fun games and challenges
                - Encourage them to start their adventure
                - Keep it conversational, enthusiastic, and age-appropriate (8-18 years)
                - Maximum 120 words
                - Use emojis sparingly but effectively

                Return only the speech text, nothing else.
            """,
            
            AyoraContext.MODULE_EXPLANATION: f"""
                You are Ayora explaining a cybersecurity module to a student. 
                Module: {context_data.get('module_name', 'Cybersecurity Basics') if context_data else 'Cybersecurity Basics'}
                
                Provide a brief, encouraging explanation of what they'll learn in this module.
                Keep it under 80 words and make it exciting for kids aged 8-18.
                
                Return only the speech text, nothing else.
            """,
            
            AyoraContext.QUIZ_ENCOURAGEMENT: """
                You are Ayora providing encouragement before a cybersecurity quiz.
                Give a short, motivating message about doing their best and learning from the experience.
                Keep it under 60 words and upbeat for kids aged 8-18.
                
                Return only the speech text, nothing else.
            """,
            
            AyoraContext.ACHIEVEMENT_CELEBRATION: f"""
                You are Ayora celebrating a student's achievement.
                Achievement: {context_data.get('achievement', 'completing a challenge') if context_data else 'completing a challenge'}
                
                Provide enthusiastic congratulations and encourage them to keep learning.
                Keep it under 70 words and very celebratory for kids aged 8-18.
                
                Return only the speech text, nothing else.
            """,
            
            AyoraContext.HELP_GUIDANCE: """
                You are Ayora providing helpful guidance to a student who might be confused.
                Give reassuring, helpful advice about learning cybersecurity step by step.
                Keep it under 80 words and supportive for kids aged 8-18.
                
                Return only the speech text, nothing else.
            """
        }
        
        try:
            # OpenAI v1 API format
            if not self.openai_client:
                raise Exception("OpenAI client not available")
                
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Ayora, an AI cybersecurity education companion for kids."},
                    {"role": "user", "content": prompts[context]}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating speech with OpenAI: {e}")
            # Fallback responses
            fallbacks = {
                AyoraContext.LANDING_INTRODUCTION: "Hi there! I'm Ayora, your friendly cybersecurity guide! 🌟 Welcome to CyberQuestJR, where learning about online safety is super fun! I'll be with you every step of the way as we explore amazing cybersecurity adventures together. Ready to become a cyber hero? Let's start your exciting journey! 🚀",
                AyoraContext.MODULE_EXPLANATION: "Great choice! This module will teach you awesome skills to stay safe online. Let's dive in and discover something amazing together! 🎯",
                AyoraContext.QUIZ_ENCOURAGEMENT: "You've got this! Take your time, think through each question, and remember - every answer helps you learn something new! 💪",
                AyoraContext.ACHIEVEMENT_CELEBRATION: "Fantastic work! You're becoming an amazing cyber hero! Keep up the incredible learning! 🏆⭐",
                AyoraContext.HELP_GUIDANCE: "No worries at all! Learning is a journey, and I'm here to help. Take it one step at a time, and you'll do great! 🤗"
            }
            return fallbacks.get(context, "Hi! I'm Ayora, and I'm excited to learn with you!")

    def calculate_animation_sequence(self, speech_text: str) -> List[Dict[str, Any]]:
        """Calculate the animation sequence based on speech content"""
        
        # Estimate speech duration (average 150 words per minute)
        word_count = len(speech_text.split())
        speech_duration = (word_count / 150) * 60  # Convert to seconds
        
        animation_sequence = [
            {
                "animation": AnimationState.WAVING.value,
                "duration": self.animation_config["waving_duration"],
                "start_time": 0
            },
            {
                "animation": AnimationState.TALKING.value, 
                "duration": speech_duration,
                "start_time": self.animation_config["waving_duration"]
            },
            {
                "animation": AnimationState.BREATHING_IDLE.value,
                "duration": -1,  # Infinite until next action
                "start_time": self.animation_config["waving_duration"] + speech_duration
            }
        ]
        
        return animation_sequence

    async def generate_audio_stream(self, speech_text: str) -> Optional[str]:
        """Generate audio using ElevenLabs TTS"""
        
        if not self.elevenlabs_client:
            print("ElevenLabs not available - no audio generated")
            return None
            
        try:
            # Generate audio stream
            audio_stream = self.elevenlabs_client.text_to_speech.stream(
                text=speech_text,
                voice_id=self.voice_id,
                model_id="eleven_multilingual_v2",
                voice_settings=self.voice_settings,
                output_format="mp3_22050_32"
            )
            
            # Save to file for frontend playback
            audio_dir = Path(__file__).parent.parent.parent / "public" / "Audio"
            audio_dir.mkdir(exist_ok=True)
            
            audio_filename = f"ayora_speech_{int(asyncio.get_event_loop().time())}.mp3"
            audio_path = audio_dir / audio_filename
            
            with open(audio_path, "wb") as f:
                for chunk in audio_stream:
                    if isinstance(chunk, bytes):
                        f.write(chunk)
            
            return f"/Audio/{audio_filename}"
            
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None

    async def generate_complete_response(self, context: AyoraContext, context_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate complete Ayora response with speech, animations, and audio"""
        
        # Generate speech text
        speech_text = self.generate_speech_text(context, context_data)
        
        # Calculate animation sequence
        animation_sequence = self.calculate_animation_sequence(speech_text)
        
        # Generate audio (optional)
        audio_filename = await self.generate_audio_stream(speech_text)
        
        # Calculate total duration
        total_duration = self.animation_config["waving_duration"] + (len(speech_text.split()) / 150) * 60
        
        return {
            "success": True,
            "speech_text": speech_text,
            "animation_sequence": animation_sequence,
            "companion_name": self.companion_name,
            "context": context.value,
            "estimated_duration": total_duration,
            "audio_filename": audio_filename,
            "error": None
        }

# Global instance
ayora_voice = AyoraVoiceEngine()

# Convenience functions for API
async def generate_landing_introduction() -> Dict[str, Any]:
    """Generate landing introduction"""
    return await ayora_voice.generate_complete_response(AyoraContext.LANDING_INTRODUCTION)

async def generate_contextual_speech(context: str, context_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Generate contextual speech"""
    context_map = {
        "landing_introduction": AyoraContext.LANDING_INTRODUCTION,
        "module_explanation": AyoraContext.MODULE_EXPLANATION,
        "quiz_encouragement": AyoraContext.QUIZ_ENCOURAGEMENT,
        "achievement_celebration": AyoraContext.ACHIEVEMENT_CELEBRATION,
        "help_guidance": AyoraContext.HELP_GUIDANCE
    }
    
    context_enum = context_map.get(context)
    if not context_enum:
        raise ValueError(f"Invalid context: {context}")
    
    return await ayora_voice.generate_complete_response(context_enum, context_data)
