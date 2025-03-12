"""
Sound management for Study Timer Pro
"""

import os
import pygame

class SoundManager:
    """
    Manages sound playback for the application
    """
    
    def __init__(self):
        """Initialize the sound manager"""
        # Initialize pygame mixer
        pygame.mixer.init()
        
        self.volume = 0.7  # Default volume (0.0 to 1.0)
        self.muted = False
        self.current_background_music = None
    
    def set_volume(self, volume):
        """
        Set the volume level
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        if not self.muted:
            pygame.mixer.music.set_volume(self.volume)
    
    def mute(self):
        """Mute all sounds"""
        self.muted = True
        pygame.mixer.music.set_volume(0)
    
    def unmute(self):
        """Unmute all sounds"""
        self.muted = False
        pygame.mixer.music.set_volume(self.volume)
    
    def play_sound(self, sound_path):
        """
        Play a sound effect
        
        Args:
            sound_path: Path to the sound file
        
        Returns:
            bool: True if sound was played, False otherwise
        """
        if not os.path.exists(sound_path):
            return False
        
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(0 if self.muted else self.volume)
            sound.play()
            return True
        except Exception as e:
            print(f"Error playing sound: {e}")
            return False
    
    def play_background_music(self, music_path, loop=True):
        """
        Play background music
        
        Args:
            music_path: Path to the music file
            loop: Whether to loop the music
        
        Returns:
            bool: True if music was played, False otherwise
        """
        if not os.path.exists(music_path):
            return False
        
        try:
            # Stop any currently playing music
            pygame.mixer.music.stop()
            
            # Load and play the new music
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0 if self.muted else self.volume)
            
            if loop:
                pygame.mixer.music.play(-1)  # Loop indefinitely
            else:
                pygame.mixer.music.play()
            
            self.current_background_music = music_path
            return True
        except Exception as e:
            print(f"Error playing background music: {e}")
            return False
    
    def stop_background_music(self):
        """Stop the currently playing background music"""
        pygame.mixer.music.stop()
        self.current_background_music = None
    
    def pause_background_music(self):
        """Pause the currently playing background music"""
        pygame.mixer.music.pause()
    
    def resume_background_music(self):
        """Resume the paused background music"""
        pygame.mixer.music.unpause()