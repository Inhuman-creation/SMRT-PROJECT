"""
SettingsGUI.py
Settings menu for changing options found in Settings.py
Last Edited: 11/8/2024
"""

import customtkinter as ctk
import tkinter as tk
import Settings
import logging

from WalkingWindow import WalkingWindow


class SettingsGUI:
    """
    This class contains the GUI for the Settings menu
    """

    def __init__(self, controller):
        self.controller = controller
        self.app = controller.app

        # Create a main frame for the settings page
        self.frame = ctk.CTkFrame(master=self.app, height=1000, width=1000, fg_color="#fdf3dd")
        self.frame.pack(expand=1, fill="both")

        # Creating fonts
        headerfont = ctk.CTkFont(family="Garet", size=100, weight="bold")
        labelfont = ctk.CTkFont(family="Garet", size=20, weight="bold")
        backbuttonfont = ctk.CTkFont(family="Garet", size=25, weight="bold")
        buttonfont = ctk.CTkFont(family="Garet", size=14, weight="bold")

        # button functions
        def back_function():
            self.controller.show_menu_gui()

        # Settings Page label
        self.welcome_label = ctk.CTkLabel(master=self.frame, text="Settings", font=headerfont, text_color="black")
        self.welcome_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        #starting y position for sliders
        slider_start_y = 0.35

        # Create back button
        back_button = ctk.CTkButton(
            master=self.frame, text="EXIT", font=backbuttonfont,
            width=100, height=50, command=back_function,
            fg_color="#d9534f", text_color="white", corner_radius=20  # from Choice GUI
        )
        back_button.place(relx=0.05, rely=0.05, relwidth=.1, relheight=.1, anchor=tk.CENTER)

        # apply changes button
        self.apply_changes_button = ctk.CTkButton(self.frame, text="Apply Changes", command=self.save_settings,
                                                  font=buttonfont, fg_color="#0f606b", text_color="white",
                                                  state="disabled")
        self.apply_changes_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Create the Known Word Requirement slider on the left side
        self.known_threshold_var = self.add_slider("Known Word Requirement",
                                                   min_val=Settings.KNOWN_THRESHOLD_MIN,
                                                   max_val=Settings.KNOWN_THRESHOLD_MAX,
                                                   initial=Settings.KNOWN_THRESHOLD,
                                                   relx=0.35,  # Positioned left
                                                   rely=slider_start_y)
        # Create the Correct-Incorrect Gap slider on the right side
        self.known_delta_var = self.add_slider("Correct-Incorrect Gap",
                                               min_val=Settings.KNOWN_DELTA_MIN,
                                               max_val=Settings.KNOWN_DELTA_MAX,
                                               initial=Settings.KNOWN_DELTA,
                                               relx=0.65,  # Positioned right
                                               rely=slider_start_y)

        slider_start_y += 0.12  # Move to the next row

        # Create the Spaced Repetition Amount slider on the left side
        self.srs_queue_length_var = self.add_slider("Spaced Repetition Amount",
                                                    min_val=Settings.SRS_QUEUE_LENGTH_MIN,
                                                    max_val=Settings.SRS_QUEUE_LENGTH_MAX,
                                                    initial=Settings.SRS_QUEUE_LENGTH,
                                                    relx=0.35,  # Positioned left
                                                    rely=slider_start_y)
        # Create the Study Batch Size slider on the right side
        self.walking_window_size_var = self.add_slider("Study Batch Size",
                                                       min_val=Settings.WALKING_WINDOW_SIZE_MIN,
                                                       max_val=Settings.WALKING_WINDOW_SIZE_MAX,
                                                       initial=Settings.WALKING_WINDOW_SIZE,
                                                       relx=0.65,  # Positioned right
                                                       rely=slider_start_y)

        slider_start_y += 0.12

        # dropdown menu for lang selection
        ctk.CTkLabel(self.frame, text="Language Selection", font=labelfont,
                     text_color="black").place(relx=0.6, rely=slider_start_y, anchor=tk.CENTER)
        options = ["Spanish", "French", "Arabic"]
        self.language_var = tk.StringVar(value=Settings.LANGUAGE)
        self.language_dropdown = ctk.CTkOptionMenu(self.app, values=options, variable=self.language_var,
                                                   font=labelfont, text_color="white",
                                                   fg_color="#acb87c",
                                                   button_color="#77721f",
                                                   command=self.on_change_language)
        self.language_dropdown.place(relx=0.6, rely=slider_start_y + 0.05, anchor=tk.CENTER)

        #foreign to english toggle
        ctk.CTkLabel(self.frame, text="Flashcard Display Language", font=labelfont,
                     text_color="black").place(relx=0.4, rely=slider_start_y, anchor=tk.CENTER)
        self.foreign_to_english_var = tk.BooleanVar(value=Settings.FOREIGN_TO_ENGLISH)
        self.foreign_to_english_toggle = ctk.CTkSwitch(
            self.frame, variable=self.foreign_to_english_var, onvalue=True, offvalue=False,
            text=f"{Settings.LANGUAGE}" if self.foreign_to_english_var.get() else "English",
            text_color="black",
            font=labelfont,
            fg_color="#acb87c",
            progress_color="#77721f",
            button_color="#f37d59",
            button_hover_color="#ffc24a",
            command=lambda: self.update_lang_label(self.foreign_to_english_toggle,self.foreign_to_english_var) #arguments added to attempt fixing error with toggle.
            #command=lambda: self.update_toggle_label(self.auto_tts_toggle, self.auto_tts_var)

        )
        self.foreign_to_english_toggle.place(relx=0.4, rely=slider_start_y + 0.05, anchor=tk.CENTER)
        slider_start_y += 0.10

        # auto tts toggle
        ctk.CTkLabel(self.frame, text="Auto Pronunciation", font=labelfont,
                     text_color="black").place(relx=0.4, rely=slider_start_y, anchor=tk.CENTER)
        self.auto_tts_var = tk.BooleanVar(value=Settings.AUTO_TTS)
        self.auto_tts_toggle = ctk.CTkSwitch(
            self.frame, variable=self.auto_tts_var, onvalue=True, offvalue=False,
            text="On" if self.auto_tts_var.get() else "Off",
            text_color="black",
            font=labelfont,
            fg_color="#acb87c",
            progress_color="#77721f",
            button_color="#f37d59",
            button_hover_color="#ffc24a",
            command=lambda: self.update_toggle_label(self.auto_tts_toggle, self.auto_tts_var)
        )
        self.auto_tts_toggle.place(relx=0.4, rely=slider_start_y + 0.05, anchor=tk.CENTER)

        #volume slider
        self.volume_var = self.add_slider("Volume", 0, 100, Settings.VOLUME, 0.6, slider_start_y)

    #create a slider for each setting
    def add_slider(self, label_text, min_val, max_val, initial, relx, rely):
        # Font for labels
        labelfont = ctk.CTkFont(family="Garet", size=14, weight="bold")
        headerfont = ctk.CTkFont(family="Garet", size=20, weight="bold")

        # Label for the slider
        label = ctk.CTkLabel(self.frame, text=label_text, font=headerfont, text_color="black")
        label.place(relx=relx, rely=rely, anchor=tk.CENTER)

        # Min, current, and max labels for the slider
        min_label = ctk.CTkLabel(self.frame, text=f"Min: {min_val}", font=labelfont, text_color="black")
        current_label = ctk.CTkLabel(self.frame, text=f"Current: {initial}", font=labelfont, text_color="black")
        max_label = ctk.CTkLabel(self.frame, text=f"Max: {max_val}", font=labelfont, text_color="black")

        # Slider
        slider_var = tk.IntVar(value=initial)
        slider = ctk.CTkSlider(
            self.frame,
            from_=min_val,
            to=max_val,
            variable=slider_var,
            width=300,
            command=lambda value, lbl=current_label: self.update_slider_label(lbl, value),
            fg_color="#acb87c",
            progress_color="#77721f",
            button_color="#f37d59",
            button_hover_color="#ffc24a"
        )
        slider.place(relx=relx, rely=rely + 0.04, anchor=tk.CENTER)

        # Place min, current, and max labels in a row below the slider
        min_label.place(relx=relx - 0.1, rely=rely + 0.04, anchor=tk.CENTER)  # Position min label to the left
        current_label.place(relx=relx, rely=rely + 0.06, anchor=tk.CENTER)  # Position current label in the center
        max_label.place(relx=relx + 0.1, rely=rely + 0.04, anchor=tk.CENTER)  # Position max label to the right

        # Store the current_label to update it when slider moves
        slider.current_label = current_label

        return slider_var

    #enable the apply changes button on settings change and update labels
    def update_slider_label(self, label, value):
        label.configure(text=f"Current: {int(float(value))}")
        self.apply_changes_button.configure(state="normal")

    # enable the apply changes button on settings change and update labels
    def update_lang_label(self, toggle, value):
        # Update the label based on the toggle's current state
        toggle.configure(text=f"{self.language_var.get()}" if value.get() else "English")
        self.apply_changes_button.configure(state="normal")

    #enable the apply changes button on settings change and update labels
    def update_toggle_label(self, toggle, value):
        # Update the label based on the toggle's current state
        toggle.configure(text="On" if value.get() else "Off")
        self.apply_changes_button.configure(state="normal")

    #enable the apply changes button on settings change
    def on_change_language(self, selected_value=None):
        self.apply_changes_button.configure(state="normal")
        self.update_lang_label(self.foreign_to_english_toggle, self.foreign_to_english_var)

    #save the settings and recreate walking window to reflect changes
    def save_settings(self):
        # Save dict to the current language file
        self.controller.study_window.word_dict_to_csv(f"{Settings.username}_{Settings.LANGUAGE}.csv")

        #update global settings variables with current GUI values
        Settings.KNOWN_THRESHOLD = self.known_threshold_var.get()
        Settings.KNOWN_DELTA = self.known_delta_var.get()
        Settings.SRS_QUEUE_LENGTH = self.srs_queue_length_var.get()
        Settings.WALKING_WINDOW_SIZE = self.walking_window_size_var.get()
        Settings.FOREIGN_TO_ENGLISH = self.foreign_to_english_var.get()
        Settings.LANGUAGE = self.language_var.get()
        Settings.AUTO_TTS = self.auto_tts_var.get()
        Settings.VOLUME = self.volume_var.get()

        #disable apply button once changes have been made
        self.apply_changes_button.configure(state="disabled")

        #create a new walking window with the new settings
        self.controller.study_window = WalkingWindow(size=Settings.WALKING_WINDOW_SIZE)

        #log changes
        logging.info(f"SETTINGS UPDATED:\nKNOWN THRESHOLD: {Settings.KNOWN_THRESHOLD}\nKNOWN DELTA: {Settings.KNOWN_DELTA}"
                     f"\nSRS QUEUE LENGTH: {Settings.SRS_QUEUE_LENGTH}\nWALKING WINDOW SIZE: {Settings.WALKING_WINDOW_SIZE}"
                     f"\nFOREIGN TO ENGLISH: {Settings.FOREIGN_TO_ENGLISH}\nLANGUAGE: {Settings.LANGUAGE}"
                     f"\nAUTO TTS: {Settings.AUTO_TTS}\nVOLUME: {Settings.VOLUME}")


    def destroy(self):
        self.frame.destroy()