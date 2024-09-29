"""
The Walking Window class implements the walking window of words
currently being studied by a user

For testing purposes, it currently reads words from CSV directly

Last Edited by: Zachary Kao
Last Edited: 9/29/2024
"""

import csv
import random
from Word import Word

class WalkingWindow:

    #create a walking window with max size of size
    def __init__(self, size: int):
        self.size = size
        self.words = []

    def add_word(self, word: Word):
        if len(self.words) < self.size:
            self.words.append(word)

    def read_from_csv(self, filepath: str, num_rows: int):
        with open(filepath, mode = 'r', encoding = 'utf-8') as file:
            reader = csv.reader(file)
            next(reader) #skip header row

            for index, row in enumerate(reader):
                if index >= num_rows: #break when numRows is reached
                    break
                if len(row) == 2: #ensure 2 col input
                    spanish, english = row
                    self.add_word(Word(english, spanish))

    """
    Return a random selection of unique words from the walking window
    Will not return more words than can be stored in the walking window
    Will return an empty list if walking window is empty
    
    param: count int : The number of random words to return
    return: A list of randomly selected Word objects
    """
    def get_random_words(self, count: int) -> list:
        return random.sample(self.words, min(count, len(self.words))) if self.words else []
