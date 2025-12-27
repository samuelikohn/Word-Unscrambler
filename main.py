from ctypes import windll
from json import load
from main_menu import MainMenu
from os import path
from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget


class Main:

    def go_to_page(self, page=MainMenu, destroy=None):
        setattr(self, page.__name__, page(self))

        if destroy:
            destroy.destroy()

    def __init__(self):

        # Get screen dimensions for placing widgets
        self.screen_width = windll.user32.GetSystemMetrics(0)
        self.screen_height = windll.user32.GetSystemMetrics(1)

        # Abs path to main file
        self.path = path.dirname(path.abspath(__file__))

        # Load settings
        with open(f"{self.path}/settings.json") as f:
            self.settings = load(f)

        # Load themes
        with open(f"{self.path}/style_dark.css", "r") as f:
            self.style_dark = f.read()
        with open(f"{self.path}/style_light.css", "r") as f:
            self.style_light = f.read()
        
        # Configure parent window
        self.app = QApplication([])
        self.app.setStyleSheet(getattr(self, f"style_{self.settings["theme"]}"))
        self.app.installEventFilter(KeyboardHooks(self))
        self.window = QMainWindow(
            windowTitle = "untitled word game lol",
            windowIcon = QIcon(f"{self.path}/img/icon.png")
        )
        self.window.showFullScreen()

        # Set central widget
        self.central_widget = QWidget(self.window)
        self.window.setCentralWidget(self.central_widget)

        # Init pages
        self.go_to_page()
        

class KeyboardHooks(QObject):
    def eventFilter(self, obj, event):
        if hasattr(self.main, "Game") and self.main.Game and self.main.Game.active and event.type() == QEvent.Type.KeyPress:
            match event.key():
                case Qt.Key.Key_Space:
                    self.main.Game.play_letters.shuffle()
                case Qt.Key.Key_Backspace:
                    self.main.Game.play_letters.delete_letter()
                case Qt.Key.Key_Return:
                    self.main.Game.play_letters.enter_word()
                case Qt.Key.Key_Enter:
                    self.main.Game.play_letters.enter_word()
                case Qt.Key.Key_A:
                    self.main.Game.play_letters.type_letter("A")
                case Qt.Key.Key_B:
                    self.main.Game.play_letters.type_letter("B")
                case Qt.Key.Key_C:
                    self.main.Game.play_letters.type_letter("C")
                case Qt.Key.Key_D:
                    self.main.Game.play_letters.type_letter("D")
                case Qt.Key.Key_E:
                    self.main.Game.play_letters.type_letter("E")
                case Qt.Key.Key_F:
                    self.main.Game.play_letters.type_letter("F")
                case Qt.Key.Key_G:
                    self.main.Game.play_letters.type_letter("G")
                case Qt.Key.Key_H:
                    self.main.Game.play_letters.type_letter("H")
                case Qt.Key.Key_I:
                    self.main.Game.play_letters.type_letter("I")
                case Qt.Key.Key_J:
                    self.main.Game.play_letters.type_letter("J")
                case Qt.Key.Key_K:
                    self.main.Game.play_letters.type_letter("K")
                case Qt.Key.Key_L:
                    self.main.Game.play_letters.type_letter("L")
                case Qt.Key.Key_M:
                    self.main.Game.play_letters.type_letter("M")
                case Qt.Key.Key_N:
                    self.main.Game.play_letters.type_letter("N")
                case Qt.Key.Key_O:
                    self.main.Game.play_letters.type_letter("O")
                case Qt.Key.Key_P:
                    self.main.Game.play_letters.type_letter("P")
                case Qt.Key.Key_Q:
                    self.main.Game.play_letters.type_letter("Q")
                case Qt.Key.Key_R:
                    self.main.Game.play_letters.type_letter("R")
                case Qt.Key.Key_S:
                    self.main.Game.play_letters.type_letter("S")
                case Qt.Key.Key_T:
                    self.main.Game.play_letters.type_letter("T")
                case Qt.Key.Key_U:
                    self.main.Game.play_letters.type_letter("U")
                case Qt.Key.Key_V:
                    self.main.Game.play_letters.type_letter("V")
                case Qt.Key.Key_W:
                    self.main.Game.play_letters.type_letter("W")
                case Qt.Key.Key_X:
                    self.main.Game.play_letters.type_letter("X")
                case Qt.Key.Key_Y:
                    self.main.Game.play_letters.type_letter("Y")
                case Qt.Key.Key_Z:
                    self.main.Game.play_letters.type_letter("Z")
                case Qt.Key.Key_Escape:
                    self.main.Game.esc()
            return True
        
        elif hasattr(self.main, "PauseGame") and self.main.PauseGame and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.PauseGame.esc()
            return True
        
        elif hasattr(self.main, "GameOver") and self.main.GameOver and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.GameOver.esc()
            return True
        
        elif hasattr(self.main, "QuitGame") and self.main.QuitGame and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.QuitGame.esc()
            return True
        
        elif hasattr(self.main, "EndOfLevel") and self.main.EndOfLevel and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.EndOfLevel.esc()
            return True
        
        elif hasattr(self.main, "QuitGameEOL") and self.main.QuitGameEOL and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.QuitGameEOL.esc()
            return True
        
        elif hasattr(self.main, "MainMenu") and self.main.MainMenu and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.MainMenu.esc()
            return True
        
        elif hasattr(self.main, "ExitApp") and self.main.ExitApp and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.ExitApp.esc()
            return True
        
        elif hasattr(self.main, "MainMenu") and self.main.MainMenu and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.MainMenu.esc()
            return True
        
        elif hasattr(self.main, "Settings") and self.main.Settings and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.Settings.esc()
            return True
        
        elif hasattr(self.main, "Tutorial0") and self.main.Tutorial0 and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.Tutorial0.esc()
            return True
        
        elif hasattr(self.main, "Tutorial1") and self.main.Tutorial1 and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.Tutorial1.esc()
            return True
        
        elif hasattr(self.main, "Tutorial2") and self.main.Tutorial2 and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.Tutorial2.esc()
            return True
        
        elif hasattr(self.main, "Tutorial3") and self.main.Tutorial3 and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.main.Tutorial3.esc()
            return True
        
        return super().eventFilter(obj, event)
    
    def __init__(self, main):
        super().__init__(main.app)
        self.main = main


if __name__ == "__main__":
    main = Main()
    main.window.show()
    main.app.exec()