#settings.py

# Walking Window Settings
KNOWN_THRESHOLD:int = 5 #number of times a word must be correctly identified to be marked as known
KNOWN_DELTA:int = 3 #the required difference between the times a word's correct and incorrect counts to be marked as known
SRS_QUEUE_LENGTH = 5 #the length of the spaced repetition queue
WALKING_WINDOW_SIZE = 30 #lENGTH OF WALKING WINDOW THAT PROGRESSES THE .CSV FILE
username = ""

# Study Settings
FOREIGN_TO_ENGLISH:bool = True