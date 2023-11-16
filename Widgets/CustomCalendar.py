from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from database_controller import get_notes_for_day, get_notes_for_id


class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)

        self.dates_colours_list = list()
        self.processed_ids = list()

        self.move_val_x = 12
        self.move_val_y = 9
        self.i = 0

        self.colour_dict = {
            'red': Qt.red,
            'green': Qt.green,
            'blue': Qt.blue,
            'black': Qt.black,
            'white': Qt.white,
        }

        self.res_list = list()

    def paintCell(self, painter, rect, date):
        QCalendarWidget.paintCell(self, painter, rect, date)

        self.processed_ids = list()

        self.move_val_x = 12
        self.move_val_y = 9
        self.i = 0

        self.res_list = get_notes_for_day(date, self.dates_colours_list)
        self.res_list = get_notes_for_id(self.user_id, self.res_list)

        for collection in self.res_list:
            notes_for_day = collection['notes_data']
            self.processDate(notes_for_day, painter, rect)

    def processDate(self, notes_list, painter, rect):
        for note in notes_list:
            note_dict = list(note.items())[0][1]

            if note_dict['note_id'] in self.processed_ids:
                return

            self.processed_ids.append(note_dict['note_id'])

            colour = self.colour_dict[note_dict['note_colour']]
            painter.setBrush(colour)

            self.drawCircle(painter, rect)

    def drawCircle(self, painter, rect):
        if self.i % 3 == 0:
            self.move_val_y += 6
            self.move_val_x = 12

        painter.drawEllipse(rect.topLeft() + QPoint(self.move_val_x, self.move_val_y), 6, 6)
        self.move_val_x += 6

        self.i += 1

    def setDates(self, dates: list, user_id):
        self.user_id = user_id
        self.dates_colours_list = dates
