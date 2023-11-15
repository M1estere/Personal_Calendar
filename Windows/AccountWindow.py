from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Settings import *
from DatabaseController import get_user_by_id, update_user

class AccountWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        widget = QWidget()
        layout = QVBoxLayout()

        self.user_id = user_id
        self.user = get_user_by_id(self.user_id)

        self.setWindowTitle(f"Edit Account")

        self.setMaximumSize(QSize(ACCOUNT_INFO_WINDOW_WIDTH, ACCOUNT_INFO_WINDOW_HEIGHT))
        self.setMinimumSize(QSize(ACCOUNT_INFO_WINDOW_WIDTH, ACCOUNT_INFO_WINDOW_HEIGHT))

        self.label = QLabel(self)
        self.label.setText('Edit account info')

        self.username_input_field = QLineEdit()
        self.username_input_field.setPlaceholderText('Enter a nickname...')

        self.initials_input_field = QLineEdit()
        self.initials_input_field.setPlaceholderText('Enter your name...')

        self.show_password = False
        self.password_input_field = QLineEdit()
        self.password_input_field.setEchoMode(QLineEdit.Password)
        self.password_input_field.setPlaceholderText('Enter your password...')

        self.show_password_button = QPushButton('Toggle Password')
        self.show_password_button.clicked.connect(self.toggle_password)

        self.save_settings_button = QPushButton('Save')
        self.save_settings_button.clicked.connect(self.save_info)

        self.reset_fields_button = QPushButton('Reset Fields')
        self.reset_fields_button.clicked.connect(self.reset_fields)

        self.username_input_field.setText(self.user['nickname'])
        self.initials_input_field.setText(self.user['name'])
        self.password_input_field.setText(self.user['password'])

        layout.addWidget(self.label)

        layout.addWidget(self.username_input_field)
        layout.addWidget(self.initials_input_field)
        layout.addWidget(self.password_input_field)

        layout.addWidget(self.show_password_button)

        layout.addWidget(self.save_settings_button)
        layout.addWidget(self.reset_fields_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def toggle_password(self):
        self.show_password = not self.show_password
        self.password_input_field.setEchoMode(QLineEdit.Normal if self.show_password else QLineEdit.Password)

    def save_info(self):
        initials = self.initials_input_field.text()
        nickname = self.username_input_field.text()
        password = self.password_input_field.text()

        if len(initials) < 1 or len(nickname) < 1 or len(password) < 1:
            print('Fill all fields!')
            return

        result = update_user(self.user_id, nickname, initials, password)

        if result == -1:
            print('User is not found!')
            return
        elif result == -2:
            print('Error occurred while updating user!')
            return
        else:
            print(f'Success updating user {self.user_id}')

        self.close()

    def reset_fields(self):
        self.username_input_field.clear()
        self.initials_input_field.clear()
        self.password_input_field.clear()
