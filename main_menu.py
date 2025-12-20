from game import Game
from os import listdir
from page import Page
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QLabel, QPushButton
from settings import Settings
from tutorial import Tutorial0


class MainMenu(Page):

    def __init__(self, main):
        super().__init__(main)

        # Load levels
        main.all_levels = listdir(f"{main.path}/levels")

        # Title
        self.add_widget(
            widget_class=QLabel,
            x=1 / 6,
            y=1 / 30,
            width=2 / 3,
            height=1 / 2,
            text="untitled word game lol.",
            font=1 / 20,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Start Game Button
        self.add_widget(
            widget_class=QPushButton,
            x=3 / 8,
            y=9 / 20,
            width=1 / 4,
            height=7 / 60,
            text="Start Game",
            font=1 / 20,
            connect=lambda: self.main.go_to_page(Game, self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Tutorial Button
        self.add_widget(
            widget_class=QPushButton,
            x=3 / 8,
            y=3 / 5,
            width=1 / 4,
            height=7 / 60,
            text="How to Play",
            font=1 / 20,
            connect=lambda: self.main.go_to_page(Tutorial0, self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Settings Button
        self.add_widget(
            widget_class=QPushButton,
            x=3 / 8,
            y=3 / 4,
            width=1 / 4,
            height=7 / 60,
            text="Settings",
            font=1 / 20,
            connect=lambda: self.main.go_to_page(Settings, self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Exit App Button
        self.add_widget(
            widget_class=QPushButton,
            x=9 / 10,
            y=1 / 360,
            width=63 / 640,
            height=2 / 45,
            text="Exit Game",
            font=1 / 60,
            connect=lambda: self.main.go_to_page(ExitApp, self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            esc=True
        )


class ExitApp(Page):

    def __init__(self, main):
        super().__init__(main)

        # Confirm Exit Text
        self.add_widget(
            widget_class=QLabel,
            x=0,
            y=1 / 5,
            width=1,
            height=1 / 10,
            text="Are you sure you want to exit the game?",
            font=1 / 30,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Confirm Exit Yes Button
        self.add_widget(
            widget_class=QPushButton,
            x=3 / 8,
            y=1 / 2,
            width=1 / 16,
            height=1 / 12,
            text="Yes",
            font=1 / 40,
            connect=lambda: self.main.app.quit(),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Confirm Exit No Button
        self.add_widget(
            widget_class=QPushButton,
            x=9 / 16,
            y=1 / 2,
            width=1 / 16,
            height=1 / 12,
            text="No",
            font=1 / 40,
            connect=lambda: self.main.go_to_page(destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            esc=True
        )