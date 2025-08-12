import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from elevenlabs import stream as play_stream  # helper to play streamed audio

import os
import json
import time
import base64
from typing import Dict, Any, Optional, Callable
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from elevenlabs import stream as play_stream
from speech_generator import SpeechGenerator, AyoraContext, AnimationState, ayora_speech

class AyoraVoiceEngine:
    def __init__(self):
        """Initialize Ayora's Text-to-Speech and Animation Engine"""
        # ElevenLabs API setup
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.elevenlabs_api_key:
            print("Warning: ELEVENLABS_API_KEY not found. Using fallback TTS.")
            self.tts_enabled = False
        else:
            self.client = ElevenLabs(api_key=self.elevenlabs_api_key)
            self.tts_enabled = True
            print("🎤 ElevenLabs TTS initialized successfully!")
        
        # Ayora's voice configuration
        self.voice_settings = VoiceSettings(
            stability=0.4,        # Slightly more stable for clarity
            similarity_boost=0.8, # Higher similarity for consistency
            style=0.8,           # Moderate expressiveness
            speed=1.1            # Slightly faster for engagement
        )
        
        # Ayora's voice ID (child-friendly female voice)
        self.ayora_voice_id = "Xb7hH8MSUJpSbSDYk0k2"
        
        # Animation and timing configuration
        self.animation_callbacks = {}
        self.current_animation_state = AnimationState.BREATHING_IDLE
        
        print("🤖 Ayora Voice Engine initialized!")

    def generate_and_speak_landing_intro(self, animation_callback: Callable = None) -> Dict[str, Any]:
        """Generate landing introduction and handle TTS + animations"""
        
        if not ayora_speech:
            return self._fallback_landing_experience(animation_callback)
        
        # Generate speech content using OpenAI
        speech_data = ayora_speech.generate_landing_introduction()
        
        # Execute the complete introduction sequence
        return self._execute_speech_sequence(speech_data, animation_callback)

    def generate_and_speak_contextual(self, context: AyoraContext, context_data: Dict[str, Any] = None, animation_callback: Callable = None) -> Dict[str, Any]:
        """Generate contextual speech and handle TTS + animations"""
        
        if not ayora_speech:
            return self._fallback_contextual_experience(context, animation_callback)
        
        # Generate contextual speech content
        speech_data = ayora_speech.generate_contextual_speech(context, context_data)
        
        # Execute the speech sequence
        return self._execute_speech_sequence(speech_data, animation_callback)

    def _execute_speech_sequence(self, speech_data: Dict[str, Any], animation_callback: Callable = None) -> Dict[str, Any]:
        """Execute the complete speech and animation sequence"""
        
        speech_text = speech_data.get("speech_text", "")
        animation_sequence = speech_data.get("animation_sequence", [])
        
        # Estimate speech duration (rough calculation)
        estimated_speech_duration = self._estimate_speech_duration(speech_text)
        
        # Update animation durations
        for anim in animation_sequence:
            if anim.get("duration") == "speech_duration":
                anim["duration"] = estimated_speech_duration
        
        sequence_result = {
            "success": True,
            "speech_text": speech_text,
            "estimated_duration": estimated_speech_duration,
            "animation_sequence": animation_sequence,
            "companion_name": speech_data.get("companion_name", "Ayora"),
            "context": speech_data.get("context", "unknown")
        }
        
        # Execute animation sequence if callback provided
        if animation_callback:
            self._execute_animation_sequence(animation_sequence, animation_callback)
        
        # Generate and stream TTS audio
        if self.tts_enabled:
            try:
                audio_result = self._generate_streaming_audio(speech_text)
                sequence_result.update(audio_result)
            except Exception as e:
                print(f"TTS Error: {e}")
                sequence_result["tts_error"] = str(e)
        else:
            sequence_result["audio_method"] = "fallback"
            print(f"🗣️ Ayora says: {speech_text}")
        
        return sequence_result

    def _generate_streaming_audio(self, text: str) -> Dict[str, Any]:
        """Generate streaming audio using ElevenLabs"""
        
        try:
            # Create streaming audio
            audio_stream = self.client.text_to_speech.stream(
                text=text,
                voice_id=self.ayora_voice_id,
                model_id="eleven_multilingual_v2",
                voice_settings=self.voice_settings,
                output_format="mp3_22050_32"
            )
            
            # Stream and save audio for web playback
            audio_chunks = []
            for chunk in audio_stream:
                if isinstance(chunk, bytes):
                    audio_chunks.append(chunk)
            
            # Combine audio chunks
            full_audio = b''.join(audio_chunks)
            
            # Save to public directory for web access
            audio_filename = f"ayora_speech_{int(time.time())}.mp3"
            audio_path = f"../public/Audio/{audio_filename}"
            
            with open(audio_path, "wb") as audio_file:
                audio_file.write(full_audio)
            
            # Also play directly if available
            try:
                play_stream(iter([full_audio]))
            except:
                pass  # Silent fail for direct playback
            
            return {
                "audio_generated": True,
                "audio_filename": audio_filename,
                "audio_path": audio_path,
                "audio_size": len(full_audio),
                "audio_base64": base64.b64encode(full_audio).decode('utf-8')  # For web streaming
            }
            
        except Exception as e:
            print(f"Audio generation failed: {e}")
            return {
                "audio_generated": False,
                "error": str(e)
            }

    def _execute_animation_sequence(self, animation_sequence: list, callback: Callable):
        """Execute animation sequence with proper timing"""
        
        for i, animation in enumerate(animation_sequence):
            animation_type = animation.get("animation")
            duration = animation.get("duration")
            trigger = animation.get("trigger", "immediate")
            
            # Call animation callback
            if callback:
                callback({
                    "animation": animation_type,
                    "duration": duration,
                    "sequence_index": i,
                    "trigger": trigger,
                    "total_animations": len(animation_sequence)
                })
            
            # Update current state
            if animation_type in [state.value for state in AnimationState]:
                self.current_animation_state = AnimationState(animation_type)
            
            print(f"🎭 Playing animation: {animation_type} (duration: {duration})")

    def _estimate_speech_duration(self, text: str) -> float:
        """Estimate speech duration based on text length and speaking rate"""
        # Rough estimation: average 150 words per minute, 5 characters per word
        words = len(text.split())
        chars = len(text)
        
        # Use character-based estimation for better accuracy
        estimated_seconds = (chars / 750) * 60  # ~750 chars per minute
        
        # Add buffer for natural pauses
        return max(2.0, estimated_seconds + 1.0)

    def _fallback_landing_experience(self, animation_callback: Callable = None) -> Dict[str, Any]:
        """Fallback experience when speech generator is not available"""
        
        fallback_text = """
        Hi there! I'm Ayora, your personal cybersecurity guide! 🛡️ 
        Welcome to CyberQuestJR, where learning to stay safe online is an exciting adventure! 
        I'll be right here with you every step of the way, helping you become a cyber hero through fun games and challenges. 
        Ready to start your journey to becoming a cybersecurity expert? Let's dive in and protect the digital world together! 🚀
        """
        
        fallback_sequence = [
            {"animation": "waving", "duration": 3.0, "trigger": "start"},
            {"animation": "talking", "duration": 8.0, "trigger": "after_wave"},
            {"animation": "breathing_idle", "duration": "continuous", "trigger": "after_speech"}
        ]
        
        if animation_callback:
            self._execute_animation_sequence(fallback_sequence, animation_callback)
        
        if self.tts_enabled:
            audio_result = self._generate_streaming_audio(fallback_text)
        else:
            audio_result = {"audio_generated": False}
            print(f"🗣️ Ayora says: {fallback_text}")
        
        return {
            "success": True,
            "speech_text": fallback_text,
            "animation_sequence": fallback_sequence,
            "companion_name": "Ayora",
            "context": "landing_fallback",
            **audio_result
        }

    def _fallback_contextual_experience(self, context: AyoraContext, animation_callback: Callable = None) -> Dict[str, Any]:
        """Fallback contextual experience"""
        
        fallback_text = "Hi! I'm here to help you on your cybersecurity learning journey. Let's explore together!"
        
        sequence = [
            {"animation": "talking", "duration": 4.0, "trigger": "start"},
            {"animation": "breathing_idle", "duration": "continuous", "trigger": "after_speech"}
        ]
        
        if animation_callback:
            self._execute_animation_sequence(sequence, animation_callback)
        
        return {
            "success": True,
            "speech_text": fallback_text,
            "animation_sequence": sequence,
            "companion_name": "Ayora",
            "context": context.value if context else "unknown"
        }

    def get_current_animation_state(self) -> AnimationState:
        """Get current animation state"""
        return self.current_animation_state

    def set_animation_callback(self, callback: Callable):
        """Set animation callback for external animation control"""
        self.animation_callbacks["default"] = callback

# Initialize global Ayora voice engine
try:
    ayora_voice = AyoraVoiceEngine()
    print("✅ Ayora Voice Engine ready for dynamic AI companion experience!")
except Exception as e:
    print(f"Warning: Ayora Voice Engine initialization failed: {e}")
    ayora_voice = None

# Test function for landing introduction
def test_landing_introduction():
    """Test the landing introduction sequence"""
    if ayora_voice:
        def test_animation_callback(animation_data):
            print(f"🎬 Animation: {animation_data}")
        
        result = ayora_voice.generate_and_speak_landing_intro(test_animation_callback)
        print("🎯 Landing introduction result:", json.dumps(result, indent=2))
    else:
        print("❌ Ayora Voice Engine not available for testing")

# Run test if executed directly
if __name__ == "__main__":
    test_landing_introduction()
API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=API_KEY)

speech = (
    "Yayyy! You finished the warm-up quiz! 🎉 "
    "Now buckle up, champ! We're heading into the real CyberQuest Junior adventure! 🚀 "
    "Are you ready to explore, learn, and have loads of fun? Let's gooo!"
)

# Optional: Configure voice behavior
settings = VoiceSettings(
    stability=0.3,
    similarity_boost=0.75,
    style=1.0,
    speed=1.2
)

# Stream the speech in real time
audio_stream = client.text_to_speech.stream(
    text=speech,
    voice_id="Xb7hH8MSUJpSbSDYk0k2",
    model_id="eleven_multilingual_v2",  # or other preferred model
    voice_settings=settings,
    output_format="mp3_22050_32"
)

# Option 1: Play directly (if playback utility is available)
play_stream(audio_stream)

# Option 2: Process chunks manually (e.g., for sending over network)
# for chunk in audio_stream:
#     if isinstance(chunk, bytes):
#         do_something_with(chunk)
