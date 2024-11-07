"""
The Walking Window class implements the walking window of current_words
currently being studied by a user

For testing purposes, it currently reads current_words from CSV directly

Last Edited by: Zachary Kao
Last Edited: 9/29/2024
"""

import csv
import random
from collections import deque
import logging
import Settings
from Word import Word

class WalkingWindow:

    #create a walking window with max size of size
    def __init__(self, size: int):
        self.size = size
        self.current_words = []
        self.srs_queue = deque(maxlen=Settings.SRS_QUEUE_LENGTH)

    def add_word(self, word: Word):
        if len(self.current_words) < self.size:
            self.current_words.append(word)

    def read_from_csv(self, filepath: str, num_rows: int):
        with open(filepath, mode = 'r', encoding = 'utf-8') as file:
            reader = csv.reader(file)
            next(reader) #skip header row

            for index, row in enumerate(reader):
                if index >= num_rows: #break when numRows is reached
                    break
                if len(row) == 6: #ensure 6 col input
                    spanish, english, seen, correct, incorrect, known = row

                    # Convert specific columns
                    seen = int(seen)
                    correct = int(correct)
                    incorrect = int(incorrect)
                    known = bool(int(known))  # Convert '1' to True, '0' to False

                    self.add_word(Word(english, spanish, seen, correct, incorrect, known))
        logging.info("READ FROM CSV: " + repr(self.current_words))

    """
    Return a random selection of unique current_words from the walking window
    Will not return more current_words than can be stored in the walking window
    Will return an empty list if walking window is empty
    
    param: count int : The number of random current_words to return
    return: A list of randomly selected Word objects
    """
    def get_random_words(self, count: int) -> list:
        return random.sample(self.current_words, min(count, len(self.current_words))) if self.current_words else []

    """
    Check the definition of a word in the walking window
    """
    def check_word_definition(self, flashword:Word, answer) -> bool:
        #convert Word to answer string to support both flashcard types
        if isinstance(answer, Word):
            answer = answer.english if Settings.FOREIGN_TO_ENGLISH else answer.spanish

        #support for both study modes
        if Settings.FOREIGN_TO_ENGLISH:
            correct:bool = (flashword.check_definition_english(answer))
        else:
            correct:bool = (flashword.check_definition_spanish(answer))

        if correct:
            known:bool = flashword.check_if_known()

            if known:
                #remove word from walking window and get a new word
                self.current_words.remove(flashword)
                logging.info("REMOVED FROM WALKING WINDOW: " + repr(flashword))
                #TODO: get a new word
            else:
                #remove word from current current_words and add to spaced repetition queue
                self.current_words.remove(flashword)
                logging.info("REMOVED FROM CURRENT WORDS: " + repr(flashword))

                #if SRS queue is full, pop a word back into the study window
                if len(self.srs_queue) == self.srs_queue.maxlen:
                    popped_word = self.srs_queue.popleft()
                    self.current_words.append(popped_word)
                    logging.info("MOVED FROM SRS QUEUE TO CURRENT WORDS: " + repr(popped_word))

                self.srs_queue.append(flashword)
                logging.info("ADDED TO SRS QUEUE: " + repr(flashword))

                #log current state
                logging.info("CURRENT WORDS: " + repr(self.current_words))
                logging.info("SRS QUEUE: " + repr(self.srs_queue))

        return correct

    """
    Function for the mark as known button
    Mark a word as known and remove it from the window
    """
    def mark_word_as_known(self, flashword:Word):
        flashword.set_known_word()
        self.current_words.remove(flashword)
        logging.info("REMOVED FROM WALKING WINDOW: " + repr(flashword))
        #TODO: get a new word?