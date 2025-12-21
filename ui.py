from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QSpinBox


class Button(QPushButton):

    def __init__(self, parent):
        super().__init__(parent)

    def arrow_navigation(self, left=None, right=None, up=None, down=None):
        self.arrow_left = left
        self.arrow_right = right
        self.arrow_up = up
        self.arrow_down = down

    def keyPressEvent(self, event):

        # Selection via Enter/Return
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.click()

        # Left arrow
        elif event.key() == Qt.Key.Key_Left:
            if self.arrow_left and self.arrow_left.isEnabled() and not self.arrow_left.isHidden():
                self.clearFocus()
                self.arrow_left.setFocus()

        # Right arrow
        elif event.key() == Qt.Key.Key_Right:
            if self.arrow_right and self.arrow_right.isEnabled() and not self.arrow_right.isHidden():
                self.clearFocus()
                self.arrow_right.setFocus()

        # Up arrow
        elif event.key() == Qt.Key.Key_Up:
            if self.arrow_up and self.arrow_up.isEnabled() and not self.arrow_up.isHidden():
                self.clearFocus()
                self.arrow_up.setFocus()

        # Down arrow
        elif event.key() == Qt.Key.Key_Down:
            if self.arrow_down and self.arrow_down.isEnabled() and not self.arrow_down.isHidden():
                self.clearFocus()
                self.arrow_down.setFocus()


class SpinBox(QSpinBox):

    def __init__(self, parent):
        super().__init__(parent)

    def arrow_navigation(self, left=None, right=None):
        self.arrow_left = left
        self.arrow_right = right

    def keyPressEvent(self, event):

        # Left arrow
        if event.key() == Qt.Key.Key_Left:
            if self.arrow_left and self.arrow_left.isEnabled() and not self.arrow_left.isHidden():
                self.clearFocus()
                self.arrow_left.setFocus()

        # Right arrow
        elif event.key() == Qt.Key.Key_Right:
            if self.arrow_right and self.arrow_right.isEnabled() and not self.arrow_right.isHidden():
                self.clearFocus()
                self.arrow_right.setFocus()
        
        return super().keyPressEvent(event)