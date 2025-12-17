from json import dump
from page import Page
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QLabel, QPushButton, QSpinBox


class Settings(Page):

    def __init__(self, main):
        super().__init__(main)
        self.main = main

        # Title
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 30,
            width=2 / 3,
            height=1 / 6,
            text="Settings",
            font=1 / 20,
            alignment=Qt.AlignmentFlag.AlignCenter,
            css_class="settings_title"
        )

        # Flavor text
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 10,
            width=2 / 3,
            height=1 / 6,
            text="Your changes will automatically be saved",
            font=1 / 60,
            alignment=Qt.AlignmentFlag.AlignCenter,
            css_class="settings_text"
        )

        # Return to Menu Button
        self.add_widget(
            widget_class=QPushButton,
            x=17 / 20,
            y=1 / 360,
            width=95 / 640,
            height=2 / 45,
            text="Return to Menu",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            css_class="settings_text"
        )

        # Level pass threshold text
        self.add_widget(
            widget_class=QLabel,
            text="Level Pass Threshold",
            font=1 / 60,
            x=1 / 12,
            y=3 / 8,
            width=1 / 6,
            height=1 / 18,
            css_class="settings_text"
        )

        # Level pass threshold spinbox
        self.level_pass_threshold = self.add_widget(
            widget_class=QSpinBox,
            x=7 / 24,
            y=3 / 8,
            width=1 / 8,
            height=1 / 18,
            minimum=0,
            maximum=100,
            suffix="%",
            single_step=10,
            read_only=True,
            value=int(main.settings["level_pass_threshold"] * 100),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            value_connect=self.update_level_pass_threshold
        )

        # Starting time text
        self.add_widget(
            widget_class=QLabel,
            text="Starting Time",
            font=1 / 60,
            x=1 / 12,
            y=1 / 2,
            width=1 / 6,
            height=1 / 18,
            css_class="settings_text"
        )

        # Starting time spinbox
        self.starting_time = self.add_widget(
            widget_class=QSpinBox,
            x=7 / 24,
            y=1 / 2,
            width=1 / 8,
            height=1 / 18,
            minimum=20,
            maximum=600,
            suffix=" seconds",
            single_step=10,
            read_only=True,
            value=int(main.settings["starting_time"] // 10),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            value_connect=self.update_starting_time
        )

        # Min length text
        self.add_widget(
            widget_class=QLabel,
            text="Starting Minimum\nWord Length",
            font=1 / 60,
            x=1 / 12,
            y=5 / 8,
            width=1 / 6,
            height=1 / 18,
            css_class="settings_text"
        )

        # Min length spinbox
        self.min_word_length = self.add_widget(
            widget_class=QSpinBox,
            x=7 / 24,
            y=5 / 8,
            width=1 / 8,
            height=1 / 18,
            minimum=4,
            maximum=10,
            suffix=" letters",
            read_only=True,
            value=int(main.settings["starting_min_length"]),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            value_connect=self.update_min_word_length
        )

        # Num hidden text
        self.add_widget(
            widget_class=QLabel,
            text="Starting Number of\nHidden Letters",
            font=1 / 60,
            x=7 / 12,
            y=3 / 8,
            width=1 / 6,
            height=1 / 18,
            css_class="settings_text"
        )

        # Num hidden spinbox
        self.num_hidden = self.add_widget(
            widget_class=QSpinBox,
            x=19 / 24,
            y=3 / 8,
            width=1 / 8,
            height=1 / 18,
            minimum=0,
            maximum=10,
            suffix=" letters",
            read_only=True,
            value=int(main.settings["starting_num_hidden"]),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            value_connect=self.update_num_hidden
        )

        # Num fake text
        self.add_widget(
            widget_class=QLabel,
            text="Starting Number of\nFake Letters",
            font=1 / 60,
            x=7 / 12,
            y=1 / 2,
            width=1 / 6,
            height=1 / 18,
            css_class="settings_text"
        )

        # Num fake spinbox
        self.num_fake = self.add_widget(
            widget_class=QSpinBox,
            x=19 / 24,
            y=1 / 2,
            width=1 / 8,
            height=1 / 18,
            minimum=0,
            maximum=10,
            suffix=" letters",
            read_only=True,
            value=int(main.settings["starting_num_fake"]),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            value_connect=self.update_num_fake
        )

        # Levels per buff text
        self.add_widget(
            widget_class=QLabel,
            text="Levels Between Each\nDifficulty Increase",
            font=1 / 60,
            x=7 / 12,
            y=5 / 8,
            width=1 / 6,
            height=1 / 18,
            css_class="settings_text"
        )

        # Levels per buff spinbox
        self.levels_per_buff = self.add_widget(
            widget_class=QSpinBox,
            x=19 / 24,
            y=5 / 8,
            width=1 / 8,
            height=1 / 18,
            minimum=1,
            maximum=10,
            suffix=" levels",
            read_only=True,
            value=int(main.settings["levels_per_buff"]),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            value_connect=self.update_levels_per_buff
        )

        # Theme text
        self.add_widget(
            widget_class=QLabel,
            text="Theme",
            font=1 / 60,
            x=1 / 4,
            y=6 / 8,
            width=1 / 12,
            height=1 / 18,
            css_class="settings_text"
        )

        # Theme button
        self.theme_button = self.add_widget(
            widget_class=QPushButton,
            text=self.main.settings["theme"].title(),
            font=1 / 60,
            x=1 / 3,
            y=6 / 8,
            width=1 / 12,
            height=1 / 18,
            connect=self.toggle_theme,
            css_class="settings_text"
        )

        # Reset to defaults
        self.reset_button = self.add_widget(
            widget_class=QPushButton,
            text="Reset to Defaults",
            font=1 / 60,
            x=7 / 12,
            y=6 / 8,
            width=1 / 8,
            height=1 / 18,
            connect=self.reset,
            css_class="settings_text"
        )

    def reset(self):
        self.level_pass_threshold.setValue(50)
        self.starting_time.setValue(180)
        self.min_word_length.setValue(4)
        self.num_fake.setValue(0)
        self.num_hidden.setValue(0)
        self.levels_per_buff.setValue(3)

    def toggle_theme(self):
        self.main.settings["theme"] = "light" if self.main.settings["theme"] == "dark" else "dark"
        with open(f"{self.main.path}/settings.json", "w") as f:
            dump(self.main.settings, f, indent=4)
        self.main.app.setStyleSheet(getattr(self.main, f"style_{self.main.settings["theme"]}"))
        self.theme_button.setText(self.main.settings["theme"].title())

    def update_level_pass_threshold(self, value):
        self.main.settings["level_pass_threshold"] = value / 100
        with open(f"{self.main.path}/settings.json", "w") as f:
            dump(self.main.settings, f, indent=4)

    def update_levels_per_buff(self, value):
        self.main.settings["levels_per_buff"] = value
        with open(f"{self.main.path}/settings.json", "w") as f:
            dump(self.main.settings, f, indent=4)

    def update_min_word_length(self, value):
        self.main.settings["starting_min_length"] = value
        with open(f"{self.main.path}/settings.json", "w") as f:
            dump(self.main.settings, f, indent=4)

    def update_num_fake(self, value):
        self.main.settings["starting_num_fake"] = value
        with open(f"{self.main.path}/settings.json", "w") as f:
            dump(self.main.settings, f, indent=4)

    def update_num_hidden(self, value):
        self.main.settings["starting_num_hidden"] = value
        with open(f"{self.main.path}/settings.json", "w") as f:
            dump(self.main.settings, f, indent=4)

    def update_starting_time(self, value):
        self.main.settings["starting_time"] = value * 10
        with open(f"{self.main.path}/settings.json", "w") as f:
            dump(self.main.settings, f, indent=4)