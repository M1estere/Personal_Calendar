from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows.MainWindow import MainWindow
from Windows.LoginWindow import LoginWindow
from DatabaseController import add_user
from Settings import *


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle('Register Window')

        self.setMaximumSize(QSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT))
        self.setMinimumSize(QSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT))

        self.label = QLabel(self)
        self.label.setText('REGISTER')
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMaximumSize(QSize(LOGIN_WINDOW_WIDTH, 70))

        self.nickname_input_field = QLineEdit()
        self.nickname_input_field.setPlaceholderText('Enter your nickname...')

        self.name_input_field = QLineEdit()
        self.name_input_field.setPlaceholderText('Enter your name...')

        self.password_input_field = QLineEdit()
        self.password_input_field.setEchoMode(QLineEdit.Password)
        self.password_input_field.setPlaceholderText('Enter your password...')

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_login_data)
        self.submit_button.setMinimumSize(QSize(LOGIN_WINDOW_WIDTH - 20, 30))

        self.reset_fields_button = QPushButton('Reset Fields')
        self.reset_fields_button.clicked.connect(self.reset_fields)
        self.reset_fields_button.setMinimumSize(QSize(LOGIN_WINDOW_WIDTH - 20, 30))

        self.alr_reg_label = QLabel()
        self.alr_reg_label.setText('Already registered?')
        self.alr_reg_label.setAlignment(Qt.AlignCenter)
        self.alr_reg_label.setMaximumSize(QSize(LOGIN_WINDOW_WIDTH, 70))

        self.login_dir_button = QPushButton('Login')
        self.login_dir_button.clicked.connect(self.open_login_page)
        self.login_dir_button.setMinimumSize(QSize(LOGIN_WINDOW_WIDTH - 20, 30))

        layout.addWidget(self.label)

        layout.addWidget(self.name_input_field)
        layout.addWidget(self.nickname_input_field)
        layout.addWidget(self.password_input_field)

        layout.addWidget(self.submit_button)
        layout.addWidget(self.reset_fields_button)

        layout.addWidget(self.alr_reg_label)
        layout.addWidget(self.login_dir_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def submit_login_data(self):
        nickname = self.nickname_input_field.text()
        name = self.name_input_field.text()
        password = self.password_input_field.text()

        user_id = add_user(nickname, name, password)

        if user_id == -1:
            print('Registration Failed, user already exists!')
            self.reset_fields()
        elif user_id == -2:
            print('Registration Failed, some error occurred!')
            self.reset_fields()
        else:
            print(f'Data Submitted for user\n\tNickname: {nickname}\n\tName: {name}\n\tPassword: {password}')
            self.close()

            self.main_window = MainWindow(user_id)
            self.main_window.show()

    def open_login_page(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()
        self.close()

    def reset_fields(self):
        self.nickname_input_field.clear()
        self.name_input_field.clear()
        self.password_input_field.clear()
