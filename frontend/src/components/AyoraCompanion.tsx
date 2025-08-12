import React, { useEffect, useState, useRef, useCallback } from 'react';
import { api } from '../services/api';

interface AyoraAnimation {
  animation: 'breathing_idle' | 'waving' | 'talking';
  duration: number | string;
  trigger: string;
}

interface AyoraSpeechData {
  success: boolean;
  speech_text: string;
  animation_sequence: AyoraAnimation[];
  companion_name: string;
  context: string;
  estimated_duration: number;
  audio_filename?: string;
  error?: string;
}

interface AyoraCompanionProps {
  context?: 'landing' | 'module_explanation' | 'quiz_encouragement' | 'achievement_celebration' | 'help_guidance';
  contextData?: any;
  onAnimationChange?: (animation: string) => void;
  onSpeechStart?: () => void;
  onSpeechEnd?: () => void;
  autoStart?: boolean;
}

const AyoraCompanion: React.FC<AyoraCompanionProps> = ({
  context = 'landing',
  contextData,
  onAnimationChange,
  onSpeechStart,
  onSpeechEnd,
  autoStart = true
}) => {
  const [currentAnimation, setCurrentAnimation] = useState<string>('breathing_idle');
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [speechData, setSpeechData] = useState<AyoraSpeechData | null>(null);
  const [audioError, setAudioError] = useState<string | null>(null);
  
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const animationTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Animation mapping for Three.js avatar
  const animationMap = {
    'breathing_idle': 'Breathing Idle',
    'waving': 'Waving (1)',
    'talking': 'Talking (1)'
  };

  const handleAnimationChange = useCallback((newAnimation: string) => {
    setCurrentAnimation(newAnimation);
    if (onAnimationChange) {
      onAnimationChange(animationMap[newAnimation as keyof typeof animationMap] || newAnimation);
    }
  }, [onAnimationChange]);

  const executeAnimationSequence = useCallback((sequence: AyoraAnimation[], speechDuration: number = 0) => {
    let currentTime = 0;

    sequence.forEach((anim, index) => {
      const delay = currentTime * 1000; // Convert to milliseconds
      
      setTimeout(() => {
        let duration = anim.duration;
        
        // Handle dynamic duration
        if (duration === 'speech_duration') {
          duration = speechDuration;
        } else if (duration === 'continuous') {
          duration = 999999; // Very long duration for continuous animations
        }

        console.log(`🎭 Playing animation: ${anim.animation} for ${duration}s`);
        handleAnimationChange(anim.animation);

        // Set next animation if not continuous
        if (anim.duration !== 'continuous' && typeof duration === 'number') {
          setTimeout(() => {
            // Check if this is the last animation or if next animation should start
            const nextAnim = sequence[index + 1];
            if (nextAnim && nextAnim.trigger === 'after_speech') {
              // Wait for speech to end before starting next animation
              return;
            }
            if (!nextAnim) {
              // Default to breathing idle when sequence ends
              handleAnimationChange('breathing_idle');
            }
          }, duration * 1000);
        }
      }, delay);

      // Update current time for next animation
      if (typeof anim.duration === 'number') {
        currentTime += anim.duration;
      }
    });
  }, [handleAnimationChange]);

  const playAudio = useCallback((audioFilename: string) => {
    if (!audioFilename) return;

    const audioUrl = `/Audio/${audioFilename}`;
    
    if (audioRef.current) {
      audioRef.current.pause();
    }

    const audio = new Audio(audioUrl);
    audioRef.current = audio;

    audio.addEventListener('loadstart', () => {
      console.log('🎵 Audio loading started');
    });

    audio.addEventListener('canplaythrough', () => {
      console.log('🎵 Audio ready to play');
      setIsPlaying(true);
      if (onSpeechStart) onSpeechStart();
      audio.play().catch(err => {
        console.error('Audio play failed:', err);
        setAudioError('Failed to play audio');
      });
    });

    audio.addEventListener('ended', () => {
      console.log('🎵 Audio ended');
      setIsPlaying(false);
      if (onSpeechEnd) onSpeechEnd();
      
      // Transition to breathing idle after speech
      setTimeout(() => {
        handleAnimationChange('breathing_idle');
      }, 500);
    });

    audio.addEventListener('error', (e) => {
      console.error('Audio error:', e);
      setAudioError('Audio playback error');
      setIsPlaying(false);
      if (onSpeechEnd) onSpeechEnd();
    });

  }, [handleAnimationChange, onSpeechStart, onSpeechEnd]);

  const startLandingIntroduction = useCallback(async () => {
    try {
      console.log('🚀 Starting Ayora landing introduction...');
      
      const response = await api.post('/api/ayora/landing-introduction');
      const data: AyoraSpeechData = response.data;
      
      if (!data.success) {
        console.error('Failed to generate landing introduction:', data.error);
        setAudioError(data.error || 'Failed to generate speech');
        return;
      }

      setSpeechData(data);
      console.log('🤖 Ayora says:', data.speech_text);

      // Execute animation sequence
      executeAnimationSequence(data.animation_sequence, data.estimated_duration);

      // Play audio if available
      if (data.audio_filename) {
        setTimeout(() => {
          playAudio(data.audio_filename!);
        }, 3000); // Start audio after waving animation (3 seconds)
      } else {
        console.log('📢 No audio file generated, showing text only');
      }

    } catch (error) {
      console.error('Error starting landing introduction:', error);
      setAudioError('Failed to connect to Ayora service');
    }
  }, [executeAnimationSequence, playAudio]);

  const startContextualSpeech = useCallback(async (context: string, contextData?: any) => {
    try {
      console.log(`🗣️ Starting Ayora contextual speech for: ${context}`);
      
      const response = await api.post('/api/ayora/contextual-speech', {
        context,
        context_data: contextData,
        trigger_animations: true
      });
      
      const data: AyoraSpeechData = response.data;
      
      if (!data.success) {
        console.error('Failed to generate contextual speech:', data.error);
        setAudioError(data.error || 'Failed to generate speech');
        return;
      }

      setSpeechData(data);
      console.log('🤖 Ayora says:', data.speech_text);

      // Execute animation sequence
      executeAnimationSequence(data.animation_sequence, data.estimated_duration);

      // Play audio if available
      if (data.audio_filename) {
        playAudio(data.audio_filename);
      }

    } catch (error) {
      console.error('Error starting contextual speech:', error);
      setAudioError('Failed to connect to Ayora service');
    }
  }, [executeAnimationSequence, playAudio]);

  // Auto-start based on context
  useEffect(() => {
    if (!autoStart) return;

    if (context === 'landing') {
      startLandingIntroduction();
    } else {
      startContextualSpeech(context, contextData);
    }
  }, [context, contextData, autoStart, startLandingIntroduction, startContextualSpeech]);

  // Cleanup
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
      if (animationTimeoutRef.current) {
        clearTimeout(animationTimeoutRef.current);
      }
    };
  }, []);

  return (
    <div className="ayora-companion-container">
      {/* Speech Text Display (for debugging or subtitle display) */}
      {speechData && (
        <div className="hidden lg:block fixed bottom-4 left-4 max-w-md bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-lg p-4 border border-purple-200 dark:border-purple-700 shadow-lg">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-bold">A</span>
              </div>
            </div>
            <div className="flex-1">
              <div className="text-sm font-medium text-gray-900 dark:text-white mb-1">
                {speechData.companion_name}
              </div>
              <div className="text-sm text-gray-700 dark:text-gray-300">
                {speechData.speech_text}
              </div>
              {isPlaying && (
                <div className="mt-2 flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-xs text-green-600 dark:text-green-400">Speaking...</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Error Display */}
      {audioError && (
        <div className="fixed bottom-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg shadow-lg">
          <div className="flex items-center">
            <span className="text-sm">⚠️ {audioError}</span>
            <button 
              onClick={() => setAudioError(null)}
              className="ml-4 text-red-500 hover:text-red-700"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Current Animation Display (for debugging) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed top-4 right-4 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-2 rounded-lg text-sm">
          🎭 Animation: {currentAnimation}
        </div>
      )}
    </div>
  );
};

export default AyoraCompanion;
