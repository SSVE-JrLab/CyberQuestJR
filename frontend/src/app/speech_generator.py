import os
import openai
from typing import Dict, Any, Optional
from enum import Enum
import json

# Set OpenAI API key from the existing key in the file
openai.api_key = "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"

class AnimationState(Enum):
    BREATHING_IDLE = "breathing_idle"
    WAVING = "waving"
    TALKING = "talking"

class AyoraContext(Enum):
    LANDING_INTRODUCTION = "landing_introduction"
    MODULE_EXPLANATION = "module_explanation"
    QUIZ_ENCOURAGEMENT = "quiz_encouragement"
    ACHIEVEMENT_CELEBRATION = "achievement_celebration"
    HELP_GUIDANCE = "help_guidance"

class SpeechGenerator:
    def __init__(self):
        """Initialize the OpenAI Speech Generator for Ayora AI Companion"""
        self.companion_name = "Ayora"
        
        # Animation timing configuration
        self.animation_config = {
            "waving_duration": 3.0,  # seconds
            "talking_buffer": 0.5,   # seconds before/after speech
        }
        
        print(f"🤖 {self.companion_name} Speech Generator initialized successfully!")

    def generate_landing_introduction(self) -> Dict[str, Any]:
        """Generate Ayora's landing page introduction with animation sequence"""
        
        prompt = f"""
        You are Ayora, a friendly and enthusiastic AI companion for CyberQuestJR, a cybersecurity education platform for kids aged 8-18. 

        Generate a warm, welcoming introduction for when a user first lands on the website. Include:
        - Introduce yourself as Ayora, their personal cyber security guide
        - Welcome them to CyberQuestJR in an exciting, kid-friendly way
        - Briefly explain that you'll be helping them throughout their cybersecurity learning journey
        - Mention that they'll learn to protect themselves online through fun games and challenges
        - Encourage them to start their adventure
        - Keep it conversational, enthusiastic, and age-appropriate (8-18 years)
        - Maximum 150 words
        - Use emojis sparingly but effectively
        
        Write in a friendly, encouraging tone that makes cybersecurity sound fun and accessible.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Ayora, an enthusiastic AI companion for kids learning cybersecurity. Be warm, encouraging, and make learning sound exciting."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8,
                top_p=0.9
            )
            
            speech_text = response.choices[0].message.content.strip()
            
            # Create animation sequence for landing introduction
            animation_sequence = [
                {
                    "animation": AnimationState.WAVING.value,
                    "duration": self.animation_config["waving_duration"],
                    "trigger": "start"
                },
                {
                    "animation": AnimationState.TALKING.value,
                    "duration": "speech_duration",  # Will be calculated by TTS
                    "trigger": "after_wave"
                },
                {
                    "animation": AnimationState.BREATHING_IDLE.value,
                    "duration": "continuous",
                    "trigger": "after_speech"
                }
            ]
            
            return {
                "context": AyoraContext.LANDING_INTRODUCTION.value,
                "speech_text": speech_text,
                "animation_sequence": animation_sequence,
                "companion_name": self.companion_name,
                "generated_at": "landing",
                "priority": "high"  # Landing intro has high priority
            }
            
        except Exception as e:
            print(f"Error generating landing introduction: {e}")
            return self._get_fallback_landing_intro()

    def generate_contextual_speech(self, context: AyoraContext, context_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate contextual speech based on user's current activity"""
        
        context_prompts = {
            AyoraContext.MODULE_EXPLANATION: self._get_module_explanation_prompt(context_data),
            AyoraContext.QUIZ_ENCOURAGEMENT: self._get_quiz_encouragement_prompt(context_data),
            AyoraContext.ACHIEVEMENT_CELEBRATION: self._get_achievement_celebration_prompt(context_data),
            AyoraContext.HELP_GUIDANCE: self._get_help_guidance_prompt(context_data)
        }
        
        prompt = context_prompts.get(context, "Provide helpful guidance to the user.")
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are {self.companion_name}, a helpful AI companion for cybersecurity education. Be encouraging, clear, and age-appropriate for kids 8-18."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7,
                top_p=0.9
            )
            
            speech_text = response.choices[0].message.content.strip()
            
            # Standard talking animation for contextual speech
            animation_sequence = [
                {
                    "animation": AnimationState.TALKING.value,
                    "duration": "speech_duration",
                    "trigger": "start"
                },
                {
                    "animation": AnimationState.BREATHING_IDLE.value,
                    "duration": "continuous",
                    "trigger": "after_speech"
                }
            ]
            
            return {
                "context": context.value,
                "speech_text": speech_text,
                "animation_sequence": animation_sequence,
                "companion_name": self.companion_name,
                "generated_at": context_data.get("current_page", "unknown") if context_data else "unknown",
                "priority": "normal"
            }
            
        except Exception as e:
            print(f"Error generating contextual speech: {e}")
            return self._get_fallback_contextual_speech(context)

    def _get_module_explanation_prompt(self, data: Dict[str, Any]) -> str:
        module_name = data.get("module_name", "this module") if data else "this module"
        return f"""
        The user is about to start learning about {module_name} in CyberQuestJR. 
        As Ayora, give them a brief, encouraging explanation of what they'll learn and why it's important for staying safe online.
        Keep it under 100 words and make it exciting.
        """

    def _get_quiz_encouragement_prompt(self, data: Dict[str, Any]) -> str:
        quiz_type = data.get("quiz_type", "quiz") if data else "quiz"
        return f"""
        The user is about to take a {quiz_type} in CyberQuestJR.
        As Ayora, encourage them and let them know you believe in them.
        Give them confidence and remind them that learning is a journey.
        Keep it under 80 words and upbeat.
        """

    def _get_achievement_celebration_prompt(self, data: Dict[str, Any]) -> str:
        achievement = data.get("achievement", "completing a challenge") if data else "completing a challenge"
        return f"""
        The user just achieved: {achievement} in CyberQuestJR.
        As Ayora, celebrate their success enthusiastically and encourage them to keep learning.
        Make them feel proud of their progress.
        Keep it under 70 words and very positive.
        """

    def _get_help_guidance_prompt(self, data: Dict[str, Any]) -> str:
        current_page = data.get("current_page", "the platform") if data else "the platform"
        return f"""
        The user needs help while on {current_page} in CyberQuestJR.
        As Ayora, offer helpful guidance and let them know you're here to support their learning.
        Be reassuring and provide clear next steps.
        Keep it under 90 words and supportive.
        """

    def _get_fallback_landing_intro(self) -> Dict[str, Any]:
        """Fallback introduction when OpenAI API fails"""
        fallback_text = f"""
        Hi there! I'm {self.companion_name}, your personal cybersecurity guide! 🛡️ 
        Welcome to CyberQuestJR, where learning to stay safe online is an exciting adventure! 
        I'll be right here with you every step of the way, helping you become a cyber hero through fun games and challenges. 
        Ready to start your journey to becoming a cybersecurity expert? Let's dive in and protect the digital world together! 🚀
        """
        
        return {
            "context": AyoraContext.LANDING_INTRODUCTION.value,
            "speech_text": fallback_text,
            "animation_sequence": [
                {"animation": AnimationState.WAVING.value, "duration": 3.0, "trigger": "start"},
                {"animation": AnimationState.TALKING.value, "duration": "speech_duration", "trigger": "after_wave"},
                {"animation": AnimationState.BREATHING_IDLE.value, "duration": "continuous", "trigger": "after_speech"}
            ],
            "companion_name": self.companion_name,
            "generated_at": "landing_fallback",
            "priority": "high"
        }

    def _get_fallback_contextual_speech(self, context: AyoraContext) -> Dict[str, Any]:
        """Fallback speech for contextual scenarios"""
        fallback_texts = {
            AyoraContext.MODULE_EXPLANATION: f"Great choice! This module will teach you important skills to stay safe online. I'm here to help you every step of the way!",
            AyoraContext.QUIZ_ENCOURAGEMENT: f"You've got this! Remember, every expert was once a beginner. Take your time and trust what you've learned!",
            AyoraContext.ACHIEVEMENT_CELEBRATION: f"Fantastic work! You're becoming a real cybersecurity hero. Keep up the amazing progress!",
            AyoraContext.HELP_GUIDANCE: f"No worries, I'm here to help! Take a look around, and remember that learning is all about exploring and asking questions."
        }
        
        return {
            "context": context.value,
            "speech_text": fallback_texts.get(context, "I'm here to help you on your cybersecurity journey!"),
            "animation_sequence": [
                {"animation": AnimationState.TALKING.value, "duration": "speech_duration", "trigger": "start"},
                {"animation": AnimationState.BREATHING_IDLE.value, "duration": "continuous", "trigger": "after_speech"}
            ],
            "companion_name": self.companion_name,
            "generated_at": "fallback",
            "priority": "normal"
        }

    def get_animation_config(self) -> Dict[str, Any]:
        """Get animation configuration for frontend integration"""
        return {
            "waving_duration": self.animation_config["waving_duration"],
            "talking_buffer": self.animation_config["talking_buffer"],
            "available_animations": [state.value for state in AnimationState],
            "companion_name": self.companion_name
        }

# Initialize global speech generator instance
try:
    ayora_speech = SpeechGenerator()
    print("✅ Ayora Speech Generator ready!")
except Exception as e:
    print(f"Warning: {e}")
    ayora_speech = None

# Export for use in other modules
__all__ = ['SpeechGenerator', 'AyoraContext', 'AnimationState', 'ayora_speech']

