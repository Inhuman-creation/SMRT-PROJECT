"""
The Word class models a Word for the purposes of language learning
It contains a foreign language word and the corresponding English definition
It can check if a given definition is correct or not

Last Edited by: Zachary Kao
Last Edited: 9/29/2024
"""

class Word:
    def __init__(self, english: str, spanish: str):
        self.english = english
        self.spanish = spanish

    def __repr__(self):
        return f"Word(spanish = {self.spanish}, english = {self.english})"

    """
    Check if the input string matches the english definition of the word
    return: True if it matches, False otherwise
    """
    def check_definition(self, input_string: str) -> bool:
        return self.english.lower() == input_string.lower()