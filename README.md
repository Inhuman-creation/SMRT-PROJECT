# SMRT Project
## Developer Set-up Guide
1. Install the the latest 64 bit version of [python](https://www.python.org/downloads/)
2. Install [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows)
3. In PyCharm [connect your Python interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)
   1. Click "\<No interpreter\>" in the bottom right of PyCharm
   2. If you see your Python interpreter displayed, click it. Else, continue
   3. Click "Add New Interpreter >"
   4. Click "Add Local Interpreter..."
   5. In the pop-up window, select the "Existing" radio button
   6. On Windows machines, enter "C:\Windows\py.exe" in the "location" text box
   7. Press OK in the bottom right to close the pop-up
4. Install required packages with pip:
	* Windows: Run setup.bat
	* MacOS/Linux: Run setup.sh

## Feature Development Guide
The following steps should be taken to add a new feature to the Main Menu. FeatureGUI will act as a placeholder name for an actual feature.
1. Make a new .py file in the main directory of the project and name it FeatureGUI.py 
2. Inside of the newly created Python file, make a class titled the same as its file. For example, `class FeatureGUI()`
3. FeatureGUI's init function should look like this: `def __init__(self, controller):`. 
	- `controller` will usually refer to the instance of the GUI class from Main.py
4. Import the `FeatureGUI` at the top of Main.py. Example: `from FeatureGUI import FeatureGUI`
	- FYI the first time `FeatureGUI` is typed here, it refers to the file or module. The second time, it refers to the class
5. In Main.py, at the bottom of the GUI class' `__init__()` function, create a function named `show_feature_gui(self)` Example:
```
	def show_feature_gui(self):
		if self.current_frame:
			self.current_frame.destroy()
		self.current_frame = FeatureGUI(self)
```
6. In MenuGUI.py, replace a placeholder or create a new CTkbutton that has its command set to `controller.show_feature_gui()`
7. Implement your feature as described in the Software Requirements Specification. Don't forget to give the user a button to go back or to the Main Menu
