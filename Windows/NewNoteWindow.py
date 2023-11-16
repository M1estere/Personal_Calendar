from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from database_controller import add_note
from settings import *


class NewNoteWindow(QMainWindow):
    def __init__(self, current_user_id, date, main_window):
        super().__init__()

        self.date = date
        self.user_id = current_user_id
        self.main_window = main_window

        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle('New Note')
        self.setMaximumSize(QSize(NEW_NOTE_WINDOW_WIDTH, NEW_NOTE_WINDOW_HEIGHT))
        self.setMinimumSize(QSize(NEW_NOTE_WINDOW_WIDTH, NEW_NOTE_WINDOW_HEIGHT))

        self.label = QLabel(self)
        self.label.setText('Add new note')

        self.title_field = QLineEdit()
        self.title_field.setPlaceholderText('Enter a title...')

        self.note_desc_field = QPlainTextEdit(widget)
        self.note_desc_field.setPlaceholderText('Enter a description...')

        self.create_colour_buttons()

        self.add_button = QPushButton('Add Note')
        self.add_button.clicked.connect(self.add_new_note)

        self.reset_fields_button = QPushButton('Reset Fields')
        self.reset_fields_button.clicked.connect(self.reset_fields)

        layout.addWidget(self.label)

        layout.addWidget(self.title_field)
        layout.addWidget(self.note_desc_field)

        layout.addLayout(self.btn_layout)

        layout.addWidget(self.add_button)
        layout.addWidget(self.reset_fields_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.title_field.setFocus()

    def create_colour_buttons(self):
        colour_list = ['red', 'green', 'blue', 'black', 'white']
        self.note_colour = colour_list[0]

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.colour_label = QLabel(self)
        self.colour_label.setText(f'Current colour: {self.note_colour}')
        self.btn_layout.addWidget(self.colour_label)

        for i in range(len(colour_list)):
            colour = colour_list[i]
            style = (f'background-color: {colour};\n'
                     'border-width: 1px;\n'
                     'border-radius: 3px;\n'
                     'border-color: black;\n'
                     'border-style: outset;')

            colour_button = QPushButton('')

            colour_button.clicked.connect(lambda checked, arg=colour: self.pick_colour(arg))
            colour_button.setStyleSheet(style)

            self.btn_layout.addWidget(colour_button)

    def pick_colour(self, colour_val):
        self.note_colour = colour_val
        self.colour_label.setText(f'Current colour: {self.note_colour}')

    def add_new_note(self):
        note_title = self.title_field.text()
        note_desc = self.note_desc_field.toPlainText()

        if len(note_title) < 1 or len(note_desc) < 1:
            print('Fill all fields!')
            return

        month = '{:02}'.format(self.date.month())
        day = '{:02}'.format(self.date.day())
        note_creation_date = f'{self.date.year()}-{month}-{day}'
        note_creation_whole = f'{note_creation_date}'

        if add_note(self.user_id, note_title, note_desc, note_creation_whole, self.note_colour):
            print(f'Added note for\n\tUser {self.user_id}\n\tTitle {note_title}\n\tDesc {note_desc}')
            self.main_window.update_calendar()
            self.close()
        else:
            print('Failure')

    def reset_fields(self):
        self.title_field.clear()
        self.note_desc_field.clear()
