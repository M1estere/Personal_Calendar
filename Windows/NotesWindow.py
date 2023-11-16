from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from settings import *
from database_controller import get_user_notes, search_note
from Windows.NewNoteWindow import NewNoteWindow
from Windows.EditNoteWindow import EditNoteWindow


class NotesWindow(QMainWindow):
    def __init__(self, date, current_user_id, main_window):
        super().__init__()

        self.date = date
        self.user_id = current_user_id
        self.main_window = main_window

        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle(f'Notes for {self.date.year()}/{self.date.month()}/{self.date.day()}')
        self.setMaximumSize(QSize(NOTES_WINDOW_WIDTH, NOTES_WINDOW_HEIGHT))
        self.setMinimumSize(QSize(NOTES_WINDOW_WIDTH, NOTES_WINDOW_HEIGHT))

        self.scroll_inner_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_inner_widget.setLayout(self.scroll_layout)
        self.fill_notes_scroll_widget()

        self.new_note_windows = list()

        self.label = QLabel(self)
        self.label.setText(f'You are on {self.date.toString(Qt.DefaultLocaleLongDate)}')

        box_layout = QHBoxLayout()
        box_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.search_input_field = QLineEdit()
        self.search_input_field.setPlaceholderText('Enter a word from note\'s title/text...')
        self.search_input_field.setMinimumSize(QSize(200, 20))

        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_note)

        box_layout.addWidget(self.search_input_field)
        box_layout.addWidget(self.search_button)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll.setWidget(self.scroll_inner_widget)

        self.button_send = QPushButton('Create New Note')
        self.button_send.clicked.connect(self.new_note_button_clicked)

        layout.addWidget(self.label)
        layout.addLayout(box_layout)
        layout.addWidget(self.scroll)
        layout.addWidget(self.button_send)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def fill_notes_scroll_widget(self):
        self.clear_scroll()
        user_notes = get_user_notes(self.user_id, f'{self.date.year()}-{self.date.month()}-{self.date.day()}')
        if user_notes is None or len(user_notes) < 1:
            return

        for note_document in user_notes:
            self.create_note_element(note_document)

    def refill_notes(self, notes_list):
        self.clear_scroll()
        if notes_list is None or len(notes_list) < 1:
            return

        for note_document in reversed(notes_list):
            self.create_note_element(note_document)

    def create_note_element(self, note_document):
        box_layout = QHBoxLayout()
        box_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        colour_button = QPushButton()
        style = (f'background-color: {note_document["note_colour"]};\n'
                 'border-width: 1px;\n'
                 'border-radius: 3px;\n'
                 'border-color: black;\n'
                 'border-style: outset;')
        colour_button.setStyleSheet(style)
        colour_button.setMinimumSize(QSize(30, 30))
        box_layout.addWidget(colour_button)

        note_title = note_document['title']

        note_creation_year = str(note_document['creation_date'])

        text = (f' Note Title: {note_title}\n'
                f' Date: {note_creation_year}')
        button = QPushButton(text)

        button.setStyleSheet("QPushButton { text-align: left; font: bold; }")
        button.setMinimumSize(QSize(215, 60))

        button.clicked.connect(lambda checked, arg=note_document: self.note_clicked(arg))
        box_layout.addWidget(button)

        self.scroll_layout.addLayout(box_layout)

    def clear_scroll(self):
        for i in reversed(range(self.scroll_layout.count())):
            t_layout = self.scroll_layout.itemAt(i).layout()
            if t_layout is not None:
                for j in reversed(range(t_layout.count())):
                    widget_removed = t_layout.itemAt(j).widget()
                    if widget_removed is not None:
                        widget_removed.setParent(None)
                t_layout.setParent(None)

    def note_clicked(self, note):
        self.edit_note_window = EditNoteWindow(self.user_id, note, self.main_window)
        self.edit_note_window.show()

        self.close()

    def search_note(self):
        search_text = self.search_input_field.text()

        if len(search_text) < 1:
            print('Enter something to search!')
            self.fill_notes_scroll_widget()
            return

        self.search_input_field.setText('')

        notes_list = search_note(search_text, self.user_id, self.date)
        if len(notes_list) < 1:
            print('Bad search request!')
            return
        else:
            self.refill_notes(notes_list)

    def new_note_button_clicked(self):
        new_notes_window = NewNoteWindow(self.user_id, self.date, self.main_window)
        self.new_note_windows.append(new_notes_window)

        self.close()
        new_notes_window.show()
