"""
WalkingWindow.py
================
The Walking Window class implements
the walking window of current_words
currently being studied by a user

Version: 3.0
Since: 11/13/2024
"""
import csv
import random
from collections import deque
import logging
import Settings
from Word import Word

class WalkingWindow:

    def __init__(self, size: int):
        """
        Create a walking window object of a certain maximum size
        Reads in words to current words
        """

        self.last = 0  # Potential use of this variable to mark the back of window when words inside not at either end become learned
        self.front = self.last + (size - 1) #TODO: EDIT LAST AND FRONT TO NOT BE INTERDEPENDENT AND THEN STATS GUI WILL JUST FIND LAST
        self.size = size
        self.srs_queue = deque(maxlen=Settings.SRS_QUEUE_LENGTH)
        self.words_dict = self.csv_to_words_dict(csv_name = f"{Settings.username}_{Settings.LANGUAGE}.csv")
        self.current_words = []
        self.init_current_words(self.size)

    def csv_to_words_dict(self, csv_name: str):
        """
        Reads the user's CSV file into a dictionary structure

        param: csv_name : the filepath of the user's CSV
        return: words_dict : a dictionary containing all the user's word data
        """

        csv_file = open(f"UserWords/{csv_name}", encoding = 'utf-8')
        reader = csv.DictReader(csv_file)
        words_dict = dict()
        # i = 1
        for row in reader:
            # logging.info(f"Reading row {i} of {csv_name}: {row}")
            # i += 1
            try:
                foreign = row["Foreign"]
                engl = row["English"]
                seen = int(row["seen"])
                correct = int(row["correct"])
                wrong = int(row["wrong"])
                known = bool(int(row["known"]))
                words_dict[foreign] = Word(foreign, engl, seen, correct, wrong, known)
            except:
                pass
        csv_file.close()
        logging.info(f"{csv_name} loaded into dictionary.")
        return words_dict
    
    def word_dict_to_csv(self, csv_name: str):
        logging.info(f"Writing words_dict to UserWords/{csv_name}")
        csv_file = open(f"UserWords/{csv_name}", encoding = 'utf-8', mode="w")
        header = "Foreign,English,seen,correct,wrong,known\n"
        csv_file.write(header)
        for word in self.words_dict.values():
            row = ""
            row += f"{word.foreign}," 
            row += f"{word.english},"
            row += f"{int(word.count_seen)},"
            row += f"{int(word.count_correct)},"
            row += f"{int(word.count_incorrect)},"
            row += f"{int(word.is_known)}\n"
            csv_file.write(row)
        csv_file.close()
        logging.info(f"{csv_name} saved.")

    def init_current_words(self, num_words: int):
        """
        Read a specified number of words into the walking window
        from word dictionary

        param: num_words : the number of words to read
        """

        count_read:int = 0

        for key, word in self.words_dict.items():
            if count_read >= num_words: #break when num_words are added
                break

            if (not word.is_known) and (len(self.current_words) < self.size):
                self.current_words.append(word)
                count_read += 1
            else:
                self.front += 1
        logging.info(f"READ {len(self.current_words)} WORDS FROM words_dict: {repr(self.current_words)}")

    def get_random_words(self, count: int) -> list:
        """
        Return a random selection of unique current_words from the walking window
        Will not return more current_words than can be stored in the walking window
        Will return an empty list if walking window is empty

        param: count int : The number of random current_words to return
        return: A list of randomly selected Word objects
        """

        return random.sample(self.current_words, min(count, len(self.current_words))) if self.current_words else []

    def check_word_definition(self, flashword:Word, answer) -> bool:
        """
        Check the definition of a word in the walking window

        param: flashword Word : The word that is being translated
        param: answer : The word or string that is being checked against the translation of the flashword
        return: True if the answer matches the translation, false otherwise
        """

        #convert Word to answer string to support both flashcard types
        if isinstance(answer, Word):
            answer = answer.english if Settings.FOREIGN_TO_ENGLISH else answer.foreign

        #support for both study modes is provided by the Word class
        correct:bool = (flashword.check_definition(answer))

        if correct:
            known:bool = flashword.check_if_known()

            if known:
                #remove word from walking window and get a new word
                self.remove_known_word(flashword)
                logging.info("REMOVED FROM WALKING WINDOW: " + repr(flashword))
                self.add_new_word()
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

    def mark_word_as_known(self, flashword:Word):
        """
        Function for the mark as known button
        Mark a word as known and remove it from the window

        param: flashword : the Word to be marked as known
        """

        flashword.set_known_word()
        self.remove_known_word(flashword)
        logging.info("MARKED AS KNOWN AND REMOVED FROM WALKING WINDOW: " + repr(flashword))
        self.add_new_word()

    def remove_known_word(self, word: Word):
        """
        Function for removing "word" from window
        Follow up with add_new_word to add a new word to the window

        param: word : the Word to be removed
        """
        if word in self.current_words:
            self.current_words.remove(word)
            self.front += 1
        else:
            logging.warning(f"Attempted to remove a word not in current_words: {repr(word)}")

    def add_new_word(self):
        """
        Read in a single word from in front of the walking window
        """
        for i in range(self.front, self.front + self.size):
            if i >= len(self.words_dict):
                break
            word = list(self.words_dict.values())[i]
            if (not word.is_known) and (len(self.current_words) < self.size):
                self.current_words.append(word)
                logging.info("ADDED NEW WORD: " + repr(word))
                break