from json import load
from math import ceil
from page import Page
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QLabel, QScrollArea, QWidget
from random import choice, shuffle, randint
from ui import Button

class Game(Page):

    def __init__(self, main):
        super().__init__(main)
        self.main = main
        self.level_count = 1
        self.active = False
        self.level_pass_threshold = main.settings["level_pass_threshold"]
        self.time = main.settings["starting_time"]
        self.min_length = main.settings["starting_min_length"]
        self.num_hidden_letters = main.settings["starting_num_hidden"]
        self.num_fake_letters = main.settings["starting_num_fake"]
        self.levels_per_buff = main.settings["levels_per_buff"]
        self.buff = ""

        # Guessing Text Field
        guess_field = self.add_widget(
            widget_class=QLabel,
            x=1 / 20,
            y=11 / 24,
            width=9 / 10,
            height=1 / 160,
            css_class="guessed_letters"
        )
        guess_field.style().unpolish(guess_field)
        guess_field.style().polish(guess_field)

        # Pause Game Button
        pause_btn = self.add_widget(
            widget_class=Button,
            x=9 / 10,
            y=1 / 360,
            width=63 / 640,
            height=2 / 45,
            text="Pause Game",
            font=1 / 60,
            connect=self.pause_game,
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            esc=True
        )

        # Required Words Number
        self.num_req = self.add_widget(
            widget_class=QLabel,
            x=1 / 640,
            y=1 / 360,
            width=1 / 6,
            height=1 / 15,
            font=1 / 60,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Widget to hold slots for all words
        self.found_words = []
        self.scroll_interior = self.add_widget(
            widget_class=QWidget,
            x=1 / 640,
            y=1 / 2,
            width=319 / 320,
            css_class="scroll_interior"
        )

        # Scroll area for guessed words
        self.add_widget(
            widget_class=QScrollArea,
            x=1 / 640,
            y=1 / 2,
            width= 319 / 320,
            height=159 / 320,
            verticalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn,
            horizontalScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
            scroll_widget=self.scroll_interior
        )
        self.scroll_interior.style().unpolish(self.scroll_interior)
        self.scroll_interior.style().polish(self.scroll_interior)

        # Timer bar
        self.timer_bar = self.add_widget(
            widget_class=QLabel,
            x=1 / 4,
            y=11/ 240,
            width=1 / 2,
            height=1 / 30,
            css_class="timer_bar"
        )

        # Timer icon
        self.add_widget(
            widget_class=QLabel,
            x=3 / 16,
            y=1 / 16 - main.screen_width / (main.screen_height * 40),
            width=1 / 20,
            height=main.screen_width / (main.screen_height * 20),
            pixmap=f"{main.path}/img/timer_{main.settings["theme"]}.png"
        )

        # Level timer
        self.timer = self.add_widget(
            widget_class=QTimer,
            timer_connect=self.update_timer_bar
        )

        pause_btn.setFocus()

        # Start game
        self.start_level()

    def destroy(self):
        if self.play_letters.toast_label:
            self.play_letters.toast_label.deleteLater()
        self.play_letters.destroy()
        for found_word in self.found_words:
            found_word.destroy()
        self.found_words.clear()
        self.timer.stop()
        self.timer.deleteLater()
        super().destroy()

    def end_game(self):
        self.main.go_to_page(GameOver, destroy=self)

    def end_level(self):

        self.hide()

        # Delete old widgets
        self.play_letters.destroy()

        for found_word in self.found_words:
            found_word.destroy()
        self.found_words.clear()

        # Add random difficulty buff every nth level
        self.level_count += 1
        if not self.level_count % self.levels_per_buff:
            buff_int = randint(1, 4)
            match buff_int:
                case 1:
                    # Hard lower limit for time of 20 sec
                    self.time = max(self.time * 0.9, 200)
                    self.buff = "<b>TIME</b> will be decreased"
                case 2:
                    self.min_length += 1
                    self.buff = "<b>MINIMUM WORD LENGTH</b> will be increased"
                case 3:
                    self.num_hidden_letters += 1
                    self.buff = "An additional letter will be <b>HIDDEN</b>"
                case 4:
                    self.num_fake_letters += 1
                    self.buff = "A <b>FAKE</b> letter will be added"

        # EOL screen
        self.main.go_to_page(EndOfLevel)

    def hide(self):

        # Hide widgets
        if self.play_letters.toast_label:
            self.play_letters.toast_label.deleteLater()
            self.play_letters.toast_label = None
        self.play_letters.hide()
        for found_word in self.found_words:
            found_word.hide()
        for widget in self.widgets:
            widget.hide()

        # Pause timers
        self.timer.stop()

    def pause_game(self):
        self.active = False
        self.hide()
        self.main.go_to_page(PauseGame)

    def resume_game(self):
        self.main.PauseGame.destroy()
        self.show()
        self.active = True

    def show(self):

        # Show widgets
        self.play_letters.show()
        for found_word in self.found_words:
            found_word.show()
        for widget in self.widgets:
            widget.show()

        # Resume timer
        self.timer.start(100)

    def start_level(self):

        self.buff = ""
        if hasattr(self.main, "EndOfLevel") and self.main.EndOfLevel:
            self.main.EndOfLevel.destroy()

        # Choose new level
        level_word = choice(self.main.all_levels)
        self.main.all_levels.remove(level_word)
        level_length = len(level_word) - 5 # remove '.json'

        # Load level JSON
        with open(f"{self.main.path}/levels/{level_word}") as f:
            level_json = load(f)

            # If min_length is too long, only show pangrams
            if self.min_length > level_length:
                level_json["words"] = [word for word in level_json["words"] if len(word) == level_length]
            else:
                level_json["words"] = [word for word in level_json["words"] if len(word) >= self.min_length]

            self.words = {word: i for i, word in enumerate(level_json["words"])}
            self.num_words = len(level_json["words"])
            self.total_letters = sum([len(word) for word in level_json["words"]])

        # Letter tiles
        self.play_letters = PlayLetters(self.main, self, level_json["letters"])

        # Calc number of required words
        self.update_words_found()

        # Set scroll_interior height
        self.words_per_column = ceil(len(self.words) / 4)
        self.scroll_interior.resize(self.scroll_interior.width(), int((FoundWord.letter_width + 1 / 80) * (self.words_per_column + 1) * self.main.screen_height))

        # Slots for guessed words
        for i, word in enumerate(level_json["words"]):
            self.found_words.append(FoundWord(self.main, self, word, i))

        self.time_left = self.time
        self.active = True
        self.show()

    def update_timer_bar(self):
        
        # Level over when time's up
        if self.time_left <= 0:
            self.active = False
            if self.play_letters.num_found_letters >= self.total_letters * self.level_pass_threshold:
                self.end_level()
            else:
                self.end_game()

        # Update timer bar styling based on time_left value
        else:
            self.timer_bar.setStyleSheet(f"""
                background-color: qlineargradient(
                    x1: 0,
                    x2: 1,
                    stop: {(self.time_left - 1) / self.time} #81daf5,
                    stop: {self.time_left / self.time} #{"222222" if self.main.settings["theme"] == "dark" else "fafafa"}
                );
                border: 4px solid #01a9db;
            """)
            self.time_left -= 1

    def update_words_found(self):
        req = ceil(self.level_pass_threshold * self.total_letters)
        if self.play_letters.num_found_letters >= req:
            self.num_req.setText("Level Passed!")
        else:
            self.num_req.setText(f"Letters Found:\n{self.play_letters.num_found_letters} / {req}")


class PlayLetters:

    upper_y = 1 / 8
    lower_y = 3 / 8

    def __init__(self, main, game, letters):
        self.main = main
        self.game = game
        self.num_letters = len(letters)
        self.available_letters = []
        self.played_letters = []
        self.num_found_words = 0
        self.num_found_letters = 0
        self.letter_width = min(1 / 20, 1 / (1.25 * (self.num_letters + game.num_fake_letters)))
        for letter in letters:
            game.add_widget(
                widget_class=QLabel,
                width=self.letter_width,
                height=self.letter_width * main.screen_width / main.screen_height,
                text=letter,
                font=1 / 30,
                alignment=Qt.AlignmentFlag.AlignCenter,
                css_class="play_letter",
                show=False,
                letter=letter,
                is_fake=False
            )
            
            # Keep letter tiles in separate widget list for deletion between levels
            self.available_letters.append(game.widgets.pop())
        
        # Add hidden letters
        letter_idxs = [i for i in range(len(self.available_letters))]
        hidden_count = 0
        while hidden_count < game.num_hidden_letters and letter_idxs:
            j = choice(letter_idxs)
            letter_idxs.remove(j)
            self.available_letters[j].setText("?")
            hidden_count += 1

        # Add fake letters
        fakes = []
        for _ in range(game.num_fake_letters):
            fake_letter = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            game.add_widget(
                widget_class=QLabel,
                width=self.letter_width,
                height=self.letter_width * main.screen_width / main.screen_height,
                text=fake_letter,
                font=1 / 30,
                alignment=Qt.AlignmentFlag.AlignCenter,
                css_class="play_letter",
                show=False,
                letter=fake_letter,
                is_fake=False
            )
            
            # Keep letter tiles in separate widget list for deletion between levels
            fakes.append(game.widgets.pop())

        # If hidden letters leftover, roll over into fakes
        fake_idxs = [i for i in range(len(fakes))]
        while hidden_count < game.num_hidden_letters and fake_idxs:
            j = choice(fake_idxs)
            fake_idxs.remove(j)
            fakes[j].setText("?")
            hidden_count += 1

        self.available_letters.extend(fakes)
        
        # Display letters
        self.shuffle()
        for letter in self.available_letters:
            letter.show()
        
        # For handling toasts
        self.toast_label = None
        self.timer = game.add_widget(
            widget_class=QTimer,
            timer_connect=self.delete_toast
        )

    def delete_letter(self):
        if self.played_letters:
            letter = self.played_letters.pop()
            if letter.text().startswith("?"):
                letter.setText("?")
            self.available_letters.append(letter)
            self.update_upper()
            self.update_lower()

    def delete_toast(self):
        self.toast_label.deleteLater()
        self.toast_label = None
        self.timer.stop()

    def destroy(self):
        for letter in self.available_letters:
            letter.deleteLater()
        self.available_letters.clear()
        for letter in self.played_letters:
            letter.deleteLater()
        self.played_letters.clear()
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None

    def enter_word(self):
        word = "".join([letter.text()[-1] if letter.text().startswith("?") else letter.letter for letter in self.played_letters]).lower()
        if word in self.game.words:
            found_word_obj = self.game.found_words[self.game.words[word]]
            if found_word_obj.found:
                self.toast("Already found! \u274C")
            else:

                # Reveal word in lower section and flag as found
                for letter in found_word_obj.letters:
                    letter.setText(letter.letter)
                self.toast(f"{word.upper()} \u2705")
                found_word_obj.found = True

                # When pangram is found:
                if len(word) == self.num_letters:

                    # Highlight fakes
                    for letter in self.available_letters:
                        letter.setProperty("class", "fake_letter")
                        letter.style().unpolish(letter)
                        letter.style().polish(letter)
                        letter.is_fake = True

                    # Unhide letters if hidden
                    for letter in self.played_letters:
                        if letter.text().startswith("?"):
                            letter.setText(letter.letter)

                # Advance to next level when all words are found
                self.num_found_words += 1
                self.num_found_letters += len(word)
                self.game.update_words_found()
                if self.num_found_letters == self.game.total_letters:
                    self.game.end_level()
        
        else:
            self.toast("Not in word list \u274C")

        # Remove letters from guessing area
        while self.played_letters:
            self.delete_letter()

    def hide(self):

        # Hide widgets
        for letter in self.available_letters:
            letter.hide()
        for letter in self.played_letters:
            letter.hide()

        # Pause timer
        self.timer.stop()

    def show(self):
        for letter in self.available_letters:
            letter.show()
        for letter in self.played_letters:
            letter.show()

    def shuffle(self):
        shuffle(self.available_letters)
        self.update_upper()

    def toast(self, message):
        if self.toast_label:
            self.delete_toast()
        
        self.toast_label = self.game.add_widget(
            widget_class=QLabel,
            x=1 / 3,
            y=1 / 4,
            width=1 / 3,
            height=1 / 12,
            text=message,
            alignment=Qt.AlignmentFlag.AlignCenter,
            css_class="toast"
        )
        self.toast_label.style().unpolish(self.toast_label)
        self.toast_label.style().polish(self.toast_label)
        self.game.widgets.pop() # Toast may be deleted when quitting game
        self.timer.start(2000)

    def type_letter(self, typed_letter):
        for i, letter in enumerate(self.available_letters):
            if letter.text() == typed_letter and not letter.is_fake:
                self.played_letters.append(self.available_letters.pop(i))
                self.update_upper()
                self.update_lower()
                return
        
        # If no match and '?' exists, type '?'
        for i, letter in enumerate(self.available_letters):
            if letter.text() == "?":
                self.available_letters.pop(i)
                letter.setText(f"?-{typed_letter}")
                self.played_letters.append(letter)
                self.update_upper()
                self.update_lower()
                return 

    def update_lower(self):
        offset = (1 - self.letter_width * len(self.played_letters) - (len(self.played_letters) - 1) * (self.letter_width / 4)) / 2
        for i, letter in enumerate(self.played_letters):
            letter.move(int((i * 1.25 * self.letter_width + offset) * self.main.screen_width), int(self.lower_y * self.main.screen_height))

    def update_upper(self):
        offset = (1 - self.letter_width * len(self.available_letters) - (len(self.available_letters) - 1) * (self.letter_width / 4)) / 2
        for i, letter in enumerate(self.available_letters):
            letter.move(int((i * 1.25 * self.letter_width + offset) * self.main.screen_width), int(self.upper_y * self.main.screen_height))


class FoundWord:

    letter_width = 1 / 60
    x_offsets = [
        1 / 80,
        1 / 3 - (5 * letter_width),
        2 / 3 - (10 * letter_width),
        1 - (1 / 80 + 15 * letter_width)
    ]

    def __init__(self, main, game, word, index):
        self.found = False
        self.letters = []
        for i, letter in enumerate(word):
            found_letter = game.add_widget(
                widget_class=QLabel,
                parent=game.scroll_interior,
                x=self.x_offsets[index // game.words_per_column] + (i * self.letter_width),
                y=1 / 80 + (index % game.words_per_column) * (self.letter_width + 1 / 80),
                width=self.letter_width,
                height=self.letter_width * main.screen_width / main.screen_height,
                text="",
                alignment=Qt.AlignmentFlag.AlignCenter,
                css_class="found_letter",
                letter=letter.upper()
            )
            found_letter.style().unpolish(found_letter)
            found_letter.style().polish(found_letter)

            # Keep letter tiles in separate widget list for deletion between levels
            self.letters.append(game.widgets.pop())

    def destroy(self):
        for letter in self.letters:
            letter.deleteLater()
        self.letters.clear()

    def hide(self):
        for letter in self.letters:
            letter.hide()

    def show(self):
        for letter in self.letters:
            letter.show()


class GameOver(Page):

    def __init__(self, main):
        super().__init__(main)

        # Game over text
        self.add_widget(
            widget_class=QLabel,
            x=1 / 4,
            y=1 / 6,
            width=1 / 2,
            height=1 / 12,
            font=1 / 20,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text="Game Over!"
        )

        # Final level count
        self.add_widget(
            widget_class=QLabel,
            x=1 / 4,
            y=1 / 4,
            width=1 / 2,
            height=1 / 12,
            font=1 / 40,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text=f"Highest Level: {main.Game.level_count}"
        )

        # Return to menu btn
        menu_btn = self.add_widget(
            widget_class=Button,
            x=1 / 3,
            y=1 / 2,
            width=1 / 3,
            height=1 / 12,
            text="Return to Main Menu",
            connect=lambda: self.main.go_to_page(destroy=self),
            font=1 / 30,
            esc=True
        )

        menu_btn.setFocus()


class PauseGame(Page):

    def __init__(self, main):
        super().__init__(main)

        # Game paused text
        self.add_widget(
            widget_class=QLabel,
            x=1 / 4,
            y=1 / 6,
            width=1 / 2,
            height=1 / 12,
            font=1 / 20,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text="Game Paused"
        )

        # Return to game btn
        resume_btn = self.add_widget(
            widget_class=Button,
            x=1 / 3,
            y=1 / 3,
            width=1 / 3,
            height=1 / 12,
            text="Resume Game",
            connect=main.Game.resume_game,
            font=1 / 30,
            esc=True
        )

        # Quit game btn
        quit_btn = self.add_widget(
            widget_class=Button,
            x=9 / 10,
            y=1 / 360,
            width=63 / 640,
            height=2 / 45,
            text="Quit Game",
            font=1 / 60,
            connect=lambda: main.go_to_page(QuitGame, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Stat names
        self.add_widget(
            widget_class=QLabel,
            x=1 / 3,
            y=1 / 2,
            width=1 / 4,
            height=1 / 3,
            text="Current Level:\nTime per Level:\nNumber of Hidden Letters:\nNumber of Fake Letters:\nDifficulty Increase Every:",
            font=1 / 60,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Stat values
        self.add_widget(
            widget_class=QLabel,
            x=7 / 12,
            y=1 / 2,
            width=1 / 12,
            height=1 / 3,
            text=f"{main.Game.level_count}\n{int(main.Game.time // 10)} seconds\n{main.Game.num_hidden_letters}\n{main.Game.num_fake_letters}\n{main.Game.levels_per_buff} levels",
            font=1 / 60,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        # Arrow navigation
        resume_btn.arrow_navigation(up=quit_btn, down=quit_btn)
        quit_btn.arrow_navigation(up=resume_btn, down=resume_btn)

        resume_btn.setFocus()    


class QuitGame(Page):

    def __init__(self, main):
        super().__init__(main)
        self.main = main

        # Confirm Quit Text
        self.add_widget(
            widget_class=QLabel,
            x=0,
            y=1 / 5,
            width=1,
            height=1 / 10,
            text="Are you sure you want to quit?",
            font=1 / 30,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Confirm Quit Yes Button
        exit_yes_btn = self.add_widget(
            widget_class=Button,
            x=3 / 8,
            y=1 / 2,
            width=1 / 16,
            height=1 / 12,
            text="Yes",
            font=1 / 40,
            connect=self.return_to_main_menu,
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Confirm Quit No Button
        exit_no_btn = self.add_widget(
            widget_class=Button,
            x=9 / 16,
            y=1 / 2,
            width=1 / 16,
            height=1 / 12,
            text="No",
            font=1 / 40,
            connect=lambda: self.main.go_to_page(PauseGame, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            esc=True
        )

        # Arrow navigation
        exit_yes_btn.arrow_navigation(left=exit_no_btn, right=exit_no_btn)
        exit_no_btn.arrow_navigation(left=exit_yes_btn, right=exit_yes_btn)

        exit_no_btn.setFocus()

    def return_to_main_menu(self):
        self.main.Game.destroy()
        self.main.go_to_page(destroy=self)


class EndOfLevel(Page):

    def __init__(self, main):
        super().__init__(main)

        # Level complete text
        self.add_widget(
            widget_class=QLabel,
            x=1 / 4,
            y=1 / 6,
            width=1 / 2,
            height=1 / 12,
            font=1 / 20,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text="Level Complete!"
        )

        # Found word count
        self.add_widget(
            widget_class=QLabel,
            x=1 / 4,
            y=1 / 4,
            width=1 / 2,
            height=1 / 12,
            font=1 / 40,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text=f"Words Found: {main.Game.play_letters.num_found_words} / {main.Game.num_words}"
        )

        # Next level btn
        next_level_btn = self.add_widget(
            widget_class=Button,
            x=1 / 3,
            y=1 / 2,
            width=1 / 3,
            height=1 / 12,
            text="Start Next Level",
            connect=main.Game.start_level,
            font=1 / 30
        )

        # Buff text
        self.add_widget(
            widget_class=QLabel,
            x=1 / 4,
            y=6 / 10,
            width=1 / 2,
            height=1 / 12,
            font=1 / 60,
            alignment=Qt.AlignmentFlag.AlignCenter,
            text=main.Game.buff
        )

        quit_btn = self.add_widget(
            widget_class=Button,
            x=9 / 10,
            y=1 / 360,
            width=63 / 640,
            height=2 / 45,
            text="Quit Game",
            font=1 / 60,
            connect=lambda: main.go_to_page(QuitGameEOL, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            esc=True
        )

        # Arrow navigation
        next_level_btn.arrow_navigation(up=quit_btn, down=quit_btn)
        quit_btn.arrow_navigation(up=next_level_btn, down=next_level_btn)

        next_level_btn.setFocus()   


class QuitGameEOL(Page):

    def __init__(self, main):
        super().__init__(main)
        self.main = main

        # Confirm Quit Text
        self.add_widget(
            widget_class=QLabel,
            x=0,
            y=1 / 5,
            width=1,
            height=1 / 10,
            text="Are you sure you want to quit?",
            font=1 / 30,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Confirm Quit Yes Button
        exit_yes_btn = self.add_widget(
            widget_class=Button,
            x=3 / 8,
            y=1 / 2,
            width=1 / 16,
            height=1 / 12,
            text="Yes",
            font=1 / 40,
            connect=self.return_to_main_menu,
            cursor=QCursor(Qt.CursorShape.PointingHandCursor)
        )

        # Confirm Quit No Button
        exit_no_btn = self.add_widget(
            widget_class=Button,
            x=9 / 16,
            y=1 / 2,
            width=1 / 16,
            height=1 / 12,
            text="No",
            font=1 / 40,
            connect=lambda: self.main.go_to_page(EndOfLevel, destroy=self),
            cursor=QCursor(Qt.CursorShape.PointingHandCursor),
            esc=True
        )

        # Arrow navigation
        exit_yes_btn.arrow_navigation(left=exit_no_btn, right=exit_no_btn)
        exit_no_btn.arrow_navigation(left=exit_yes_btn, right=exit_yes_btn)

        exit_no_btn.setFocus()

    def return_to_main_menu(self):
        self.main.Game.destroy()
        self.main.go_to_page(destroy=self)