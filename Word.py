"""
The Word class models a Word for the purposes of lang learning
It contains a foreign lang word and the corresponding English definition
It can check if a given definition is correct or not

Last Edited: 11/8/2024
"""

import logging
import Settings

class Word:

    def __init__(self, foreign: str, english: str,
                 count_seen: int = None, count_correct: int = None,
                 count_incorrect: int = None, is_known: bool = None):
        """
        Initialize a Word object

        :param english: english definition of the word
        :param foreign: foreign definition of the word

        Count parameters can be used when reading word userdata to load previous values
        :param count_seen: number of times this word has been tested
        :param count_correct: number of times this word was correctly identified
        :param count_incorrect: number of times this word was incorrectly identified
        :param is_known: flag if this word is is_known or not
        """

        self.english = english
        self.foreign = foreign

        if count_seen is not None:
            self.count_seen = count_seen
        else:
            self.count_seen = 0

        if count_correct is not None:
            self.count_correct = count_correct
        else:
            self.count_correct = 0

        if count_incorrect is not None:
            self.count_incorrect = count_incorrect
        else:
            self.count_incorrect = 0

        if is_known is not None:
            self.is_known = is_known
        else:
            self.is_known = False

    #Simple representation of a word
    def __repr__(self):
        return f"Word({self.foreign})"

    def detailed_repr(self):
        """
        For displaying detailed status of the word
        """
        return (f"Word(foreign = {self.foreign}, english = {self.english}"
                f", count_seen = {self.count_seen}, count_correct = {self.count_correct}"
                f", count_incorrect = {self.count_incorrect}, known = {self.is_known})")

    def check_definition(self, answer):
        """
        Dynamically checks if the input matches the definition of the word
        depending on what Settings are set.
        param answer : a word or string to check against this word's definitions
        return : True if it matches, False otherwise
        """

        if isinstance(answer, Word):
            answer = answer.english if Settings.FOREIGN_TO_ENGLISH else answer.foreign

        correct = (self.english.lower() == answer.lower()) if Settings.FOREIGN_TO_ENGLISH \
            else (self.foreign.lower() == answer.lower())

        if correct:
            self.correct()
        else:
            self.incorrect()

        return correct

    def correct(self):
        """
        Function to be called when a word is correctly identified
        Increments counts seen and correct
        """

        self.count_seen += 1
        self.count_correct += 1
        logging.info("CORRECT: " + self.detailed_repr())

    def incorrect(self):
        """
        Function to be called when a word is correctly identified
        Increments counts seen and incorrect
        """

        self.count_seen += 1
        self.count_incorrect += 1
        logging.info("INCORRECT: " + self.detailed_repr())

    def set_known_word(self):
        """
        Function to be called when the word is acknowledged as is_known
        """

        self.is_known = True
        logging.info("MARKED AS KNOWN: " + self.detailed_repr())

    def check_if_known(self) -> bool:
        """
        Function to check if the word should be marked as is_known
        """

        if self.count_correct >= Settings.KNOWN_THRESHOLD:
            if (self.count_correct - self.count_incorrect) >= Settings.KNOWN_DELTA:
                #mark word as is_known
                self.set_known_word()
                return self.is_known
