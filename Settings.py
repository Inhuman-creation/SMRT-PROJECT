"""
Settings.py
================
This is the backend for the settings.
The users interactions with the SettingsGUI
are powered through here.

Version: 2.0
Since: 11-10-2024
"""

# Walking Window Settings
KNOWN_THRESHOLD:int = 5 #number of times a word must be correctly identified to be marked as known
KNOWN_DELTA:int = 3 #the required difference between the times a word's correct and incorrect counts to be marked as known
SRS_QUEUE_LENGTH = 5 #the length of the spaced repetition queue
WALKING_WINDOW_SIZE = 30 #LENGTH OF WALKING WINDOW THAT PROGRESSES THE .CSV FILE
username = ""

# Study Settings
FOREIGN_TO_ENGLISH:bool = True
LANGUAGE = "Spanish"
LANGUAGE_OPTIONS = ["Spanish", "French", "Arabic", "Japanese", "Mandarin", "Hieroglyphic"]
AUTO_TTS:bool = False
VOLUME:int = 100

# Settings Min/Max Values
KNOWN_THRESHOLD_MIN:int = 1
KNOWN_THRESHOLD_MAX:int = 20
KNOWN_DELTA_MIN:int = 0
KNOWN_DELTA_MAX:int = 10
SRS_QUEUE_LENGTH_MIN:int = 1
SRS_QUEUE_LENGTH_MAX:int = 15
WALKING_WINDOW_SIZE_MIN:int = 20
WALKING_WINDOW_SIZE_MAX:int = 50
