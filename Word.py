"""
The Word class models a Word for the purposes of language learning
It contains a foreign language word and the corresponding English definition
It can check if a given definition is correct or not

Last Edited by: Zachary Kao
Last Edited: 11/8/2024
"""

import logging
import Settings

class Word:
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
    def __init__(self, foreign: str, english: str,
                 count_seen: int = None, count_correct: int = None,
                 count_incorrect: int = None, is_known: bool = None):
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

    #For displaying detailed status of the word
    def detailed_repr(self):
        return (f"Word(foreign = {self.foreign}, english = {self.english}"
                f", count_seen = {self.count_seen}, count_correct = {self.count_correct}"
                f", count_incorrect = {self.count_incorrect}, known = {self.is_known})")


    """
    Check if the input string matches the english definition of the word
    Will call the corresponding function to update this word's count variables
    return True if it matches, False otherwise
    """
    def check_definition_english(self, input_string: str) -> bool:
        correct = self.english.lower() == input_string.lower()

        if correct:
            self.correct()
        else:
            self.incorrect()

        return correct

    """
    Check if the input string matches the foreign definition of the word
    Will call the corresponding function to update this word's count variables
    return True if it matches, False otherwise
    """
    def check_definition_foreign(self, input_string: str) -> bool:
        correct = self.foreign.lower() == input_string.lower()

        if correct:
            self.correct()
        else:
            self.incorrect()

        return correct

    """
    Function to be called when a word is correctly identified
    Increments counts seen and correct
    """
    def correct(self):
        self.count_seen += 1
        self.count_correct += 1
        logging.info("CORRECT: " + self.detailed_repr())

    """
    Function to be called when a word is correctly identified
    Increments counts seen and incorrect
    """
    def incorrect(self):
        self.count_seen += 1
        self.count_incorrect += 1
        logging.info("INCORRECT: " + self.detailed_repr())

    """
    Function to be called when the word is acknowledged as is_known
    """
    def set_known_word(self):
        self.is_known = True
        logging.info("MARKED AS KNOWN: " + self.detailed_repr())

    """
    Function to be called when the word is to be unmarked as known
    Useful if settings have changed and known state needs to be updated
    """
    def set_unknown_word(self):
        self.is_known = False
        logging.info("MARKED AS UNKNOWN: " + self.detailed_repr())

    """
    Function to check if the word should be marked as is_known
    """
    def check_if_known(self) -> bool:
        if self.count_correct >= Settings.KNOWN_THRESHOLD:
            if (self.count_correct - self.count_incorrect) >= Settings.KNOWN_DELTA:
                #mark word as is_known
                self.set_known_word()
                return self.is_known
        elif self.is_known:
            #set word back to unknown
            self.set_unknown_word()
            return self.is_known
