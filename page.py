from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QWidget


class Page:

    def __init__(self, main):
        self.main = main
        self.widgets = []

    def add_widget(self, widget_class,
            parent=None,
            x=0,
            y=0,
            width=0,
            height=0,
            show=True,
            enabled=True,
            text=None,
            font=None,
            alignment=None,
            css_class=None,
            cursor=None,
            connect=None,
            timer_connect=None,
            letter=None,
            is_fake=None,
            verticalScrollBarPolicy=None,
            horizontalScrollBarPolicy=None,
            scroll_widget=None,
            pixmap=None,
            minimum=None,
            maximum=None,
            value=None,
            suffix=None,
            single_step=None,
            value_connect=None,
            read_only=None
        ):

        new_widget = widget_class(parent) if parent else widget_class(self.main.central_widget)
        if issubclass(widget_class, QWidget):
            new_widget.setGeometry(QRect(
                int(self.main.screen_width * x),
                int(self.main.screen_height * y),
                int(self.main.screen_width * width),
                int(self.main.screen_height * height)
            ))
            new_widget.show() if show else new_widget.hide()
            new_widget.setEnabled(True) if enabled else new_widget.setEnabled(False)
            self.widgets.append(new_widget)

        if text: new_widget.setText(text)
        if font: new_widget.setFont(QFont("Trebuchet MS", int(self.main.screen_height * font)))
        if alignment: new_widget.setAlignment(alignment)
        if css_class: new_widget.setProperty("class", css_class)
        if cursor: new_widget.setCursor(cursor)
        if connect: new_widget.clicked.connect(connect)
        if timer_connect: new_widget.timeout.connect(timer_connect)
        if value_connect: new_widget.valueChanged.connect(value_connect)
        if letter: new_widget.letter = letter
        if is_fake != None: new_widget.is_fake = is_fake
        if verticalScrollBarPolicy: new_widget.setVerticalScrollBarPolicy(verticalScrollBarPolicy)
        if horizontalScrollBarPolicy: new_widget.setHorizontalScrollBarPolicy(horizontalScrollBarPolicy)
        if scroll_widget: new_widget.setWidget(scroll_widget)
        if minimum: new_widget.setMinimum(minimum)
        if maximum: new_widget.setMaximum(maximum)
        if value: new_widget.setValue(value)
        if suffix: new_widget.setSuffix(suffix)
        if single_step: new_widget.setSingleStep(single_step)
        if read_only: new_widget.lineEdit().setReadOnly(True)
        if pixmap: new_widget.setPixmap(
            QPixmap(pixmap).scaled(
                QSize(int(self.main.screen_width * width), int(self.main.screen_height * height)),
                aspectRatioMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                transformMode = Qt.TransformationMode.FastTransformation
            )
        )

        return new_widget

    def destroy(self):
        for widget in self.widgets:
            widget.deleteLater()

        setattr(self.main, self.__class__.__name__, None)