from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from database_controller import save_edited_note, delete_note
from settings import *


class EditNoteWindow(QMainWindow):
    def __init__(self, current_user_id, note, main_window):
        super().__init__()

        self.user_id = current_user_id
        self.note = note
        self.main_window = main_window

        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle(f"Edit Note {self.note['_id']}")
        self.setMaximumSize(QSize(NEW_NOTE_WINDOW_WIDTH, NEW_NOTE_WINDOW_HEIGHT))
        self.setMinimumSize(QSize(NEW_NOTE_WINDOW_WIDTH, NEW_NOTE_WINDOW_HEIGHT))

        self.label = QLabel(self)
        self.label.setText('Edit note')

        self.title_field = QLineEdit()
        self.title_field.setPlaceholderText('Enter a title...')

        self.note_desc_field = QPlainTextEdit(widget)
        self.note_desc_field.setPlaceholderText('Enter a description...')

        self.create_colour_buttons()

        self.add_button = QPushButton('Save Note')
        self.add_button.clicked.connect(self.save_note)

        self.reset_fields_button = QPushButton('Reset Fields')
        self.reset_fields_button.clicked.connect(self.reset_fields)

        self.delete_note_button = QPushButton('Delete Note')
        self.delete_note_button.clicked.connect(self.delete_note)

        layout.addWidget(self.label)

        layout.addWidget(self.title_field)
        layout.addWidget(self.note_desc_field)

        layout.addLayout(self.btn_layout)

        layout.addWidget(self.add_button)
        layout.addWidget(self.reset_fields_button)
        layout.addWidget(self.delete_note_button)

        # filling fields
        self.title_field.setText(f"{self.note['title']}")
        self.note_desc_field.setPlainText(f"{self.note['desc']}")

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.title_field.setFocus()

    def save_note(self):
        if len(self.title_field.text()) < 1:
            print('Enter any title!')
            return

        if len(self.note_desc_field.toPlainText()) < 1:
            print('Enter any description')
            return

        result = save_edited_note(self.user_id, self.note['_id'], self.title_field.text(), self.note_desc_field.toPlainText(), self.note['creation_date'], self.note_colour)

        if result == -1:
            print('Failure saving note, not existing')
        elif result == -2:
            print('Some error occurred while saving note!')
        else:
            print('Success saving note!')

        self.main_window.update_calendar()
        self.close()

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

    def delete_note(self):
        result = delete_note(self.note['creation_date'], self.note['_id'])

        if result == -1:
            print('Failure deleting note, not existing!')
            return
        elif result == -2:
            print('Some error occurred while deleting note!')
            return
        else:
            print('Success deleting note!')

        self.main_window.update_calendar()
        self.close()

    def reset_fields(self):
        self.title_field.clear()
        self.note_desc_field.clear()
