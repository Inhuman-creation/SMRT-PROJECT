"""
TextToSpeech.py
TTS Module for the SMRT Vocab app

Last Edited: 11/13/2024
"""

from gtts import gTTS
import pygame
import os
import logging
import threading
import Settings

#Base directory for audio files
BASE_AUDIO_DIR = "audio_files"
LANGUAGES = {"english": "en", "spanish": "es", "french": "fr"}

# Ensure lang-specific directories exist
for language in LANGUAGES:
    os.makedirs(os.path.join(BASE_AUDIO_DIR, language), exist_ok=True)

def get_audio_file_path(word, lang):
    """Generates a standardized path for each word's audio file based on lang."""
    return os.path.join(BASE_AUDIO_DIR, lang, f"{word}.mp3")

def generate_pronunciation(word, lang):
    """
    Generates and saves the pronunciation audio for a word if it doesn't already exist.
    :param word: The word to pronounce
    :param lang: The lang of the word ('english', 'spanish', 'french')
    """
    lang_code = LANGUAGES.get(lang.lower())
    if not lang_code:
        logging.info(f"Language '{lang.lower()}' is not supported.")
        return None

    # Get the path for the audio file
    audio_file_path = get_audio_file_path(word, lang)

    # Check if the file already exists
    if not os.path.isfile(audio_file_path):
        # Generate the pronunciation audio and save it
        tts = gTTS(text=word, lang=lang_code)
        tts.save(audio_file_path)
        logging.info(f"Saved pronunciation for '{word}' in {lang}.")
    else:
        logging.info(f"Pronunciation for '{word}' in {lang} already exists.")

    return audio_file_path

def play_audio_async(file_path):
    """Play audio file asynchronously."""

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(Settings.VOLUME/100)
    pygame.mixer.music.play()

def play_pronunciation(word, lang):
    """Generate pronunciation if needed and play it in a separate thread."""

    audio_file_path = generate_pronunciation(word, lang)

    if audio_file_path:
        # Play audio in a separate thread
        threading.Thread(target=play_audio_async, args=(audio_file_path,), daemon=True).start()
