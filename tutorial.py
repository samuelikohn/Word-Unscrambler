from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QLabel, QPushButton
from page import Page


class Tutorial0(Page):

    def __init__(self, main):
        super().__init__(main)
        
        # Title
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 30,
            width=2 / 3,
            height=1 / 6,
            text="How to Play",
            font=1 / 20,
            alignment=Qt.AlignmentFlag.AlignCenter
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
            esc=True
        )

        # Expo Dump
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 4,
            width=2 / 3,
            height=5 / 8,
            font=1 / 40,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text="<b>TYPE</b> to enter letters into the guessing area.<br/><br/>Press <b>ENTER</b> to submit a guess.<br/><br/>Press <b>BACKSPACE</b> to delete a letter.<br/><br/>Press <b>SPACE</b> to shuffle the non-guessed letters.<br/><br/><b>SCROLL</b> in the lower half of the screen to see all guessed words so far."
        )

        # Next Page Button
        self.add_widget(
            widget_class=QPushButton,
            x=17 / 20,
            y=343 / 360,
            width=95 / 640,
            height=2 / 45,
            text="Next Page",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(Tutorial1, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )


class Tutorial1(Page):

    def __init__(self, main):
        super().__init__(main)
        
        # Timer image
        self.add_widget(
            widget_class=QLabel,
            x=1 / 8,
            y=1 / 10,
            width=3 / 4,
            height=5 / 16,
            pixmap=f"{main.path}/img/tutorial_{main.settings["theme"]}.png",
            alignment=Qt.AlignmentFlag.AlignCenter,
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
            esc=True
        )

        # Expo Dump
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 4,
            width=2 / 3,
            height=5 / 8,
            font=1 / 40,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text="Using the available letters, try to find as many\nwords as possible before the timer runs out.\n\nYou must find the required number of words to pass the level,\nor it's game over.\n\nThe percentage of available words required can be changed in the settings."
        )

        # Prev Page Button
        self.add_widget(
            widget_class=QPushButton,
            x=1 / 640,
            y=343 / 360,
            width=95 / 640,
            height=2 / 45,
            text="Previous Page",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(Tutorial0, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Next Page Button
        self.add_widget(
            widget_class=QPushButton,
            x=17 / 20,
            y=343 / 360,
            width=95 / 640,
            height=2 / 45,
            text="Next Page",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(Tutorial2, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )


class Tutorial2(Page):

    def __init__(self, main):
        super().__init__(main)
        
        # Title
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 30,
            width=2 / 3,
            height=1 / 6,
            text="As you complete levels, the below difficulty\nbuffs are randomly applied one at a time.",
            font=1 / 30,
            alignment=Qt.AlignmentFlag.AlignCenter
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
            esc=True
        )

        # Buff list
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 8,
            width=2 / 3,
            height=5 / 8,
            font=1 / 40,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text="<b>TIME</b> is decreased by 10%.<br/><br/><b>MINIMUM LENGTH</b> of allowed words is increased by 1.<br/><br/>An additional letter will now be <b>HIDDEN</b>.<br/><br/>A <b>FAKE</b> letter is added."
        )

        # Expo Dump
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=2 / 3,
            width=2 / 3,
            height=1 / 6,
            text="The number of levels between each\ndifficulty buff can be changed in the settings. You can\nalso change the starting values of each difficulty buff to\nraise or lower the overall game difficulty.",
            font=1 / 40,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Prev Page Button
        self.add_widget(
            widget_class=QPushButton,
            x=1 / 640,
            y=343 / 360,
            width=95 / 640,
            height=2 / 45,
            text="Previous Page",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(Tutorial1, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Next Page Button
        self.add_widget(
            widget_class=QPushButton,
            x=17 / 20,
            y=343 / 360,
            width=95 / 640,
            height=2 / 45,
            text="Next Page",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(Tutorial3, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )


class Tutorial3(Page):

    def __init__(self, main):
        super().__init__(main)
        
        # Title
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 30,
            width=2 / 3,
            height=1 / 6,
            text="When successfully guessing the <b>PANGRAM</b>:",
            font=1 / 30,
            alignment=Qt.AlignmentFlag.AlignCenter
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
            esc=True
        )

        # Expo Dump
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 4,
            width=2 / 3,
            height=5 / 8,
            font=1 / 40,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text="All <b>HIDDEN</b> and <b>FAKE</b> letters will be revealed."
        )

        # Prev Page Button
        self.add_widget(
            widget_class=QPushButton,
            x=1 / 640,
            y=343 / 360,
            width=95 / 640,
            height=2 / 45,
            text="Previous Page",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(Tutorial2, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )