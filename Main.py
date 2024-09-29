from GUIClass import GUI
from WalkingWindow import WalkingWindow
from Word import Word

object1=GUI()

#testing walking window and word classes
study_window = WalkingWindow(size=10)
study_window.read_from_csv("Spanish.csv", num_rows=10)
random_words = study_window.get_random_words(5)
print(random_words)

#test checking definition
test_word = Word(english = 'test', spanish = 'spanishtest')
print(f"Test definition works? {test_word.check_definition('test')}")
