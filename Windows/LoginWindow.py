from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Windows.MainWindow import MainWindow
from DatabaseController import try_log_user
from Settings import *


class LoginWindow(QMainWindow):
    def __init__(self, reg_window):
        super().__init__()

        self.reg_window = reg_window

        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle('Login Window')

        self.setMaximumSize(QSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT))
        self.setMinimumSize(QSize(LOGIN_WINDOW_WIDTH, LOGIN_WINDOW_HEIGHT))

        self.label = QLabel(self)
        self.label.setText('LOGIN')
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMaximumSize(QSize(LOGIN_WINDOW_WIDTH, 70))

        self.nickname_input_field = QLineEdit()
        self.nickname_input_field.setPlaceholderText('Enter your nickname...')

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
        self.alr_reg_label.setText('Not registered yet?')
        self.alr_reg_label.setAlignment(Qt.AlignCenter)
        self.alr_reg_label.setMaximumSize(QSize(LOGIN_WINDOW_WIDTH, 70))

        self.reg_dir_button = QPushButton('Register')
        self.reg_dir_button.clicked.connect(self.open_reg_page)
        self.reg_dir_button.setMinimumSize(QSize(LOGIN_WINDOW_WIDTH - 20, 30))

        layout.addWidget(self.label)

        layout.addWidget(self.nickname_input_field)
        layout.addWidget(self.password_input_field)

        layout.addWidget(self.submit_button)
        layout.addWidget(self.reset_fields_button)

        layout.addWidget(self.alr_reg_label)
        layout.addWidget(self.reg_dir_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def submit_login_data(self):
        nickname = self.nickname_input_field.text()
        password = self.password_input_field.text()

        user_log_result = try_log_user(nickname, password)

        if user_log_result == -1:
            print('Login Failed, no such user in database!')
            self.reset_fields()
        elif user_log_result == -2:
            print('Login Failed, wrong password!')
            self.password_input_field.clear()
        else:
            print(f'Data Submitted for user\n\tNickname: {nickname}\n\tPassword: {password}')
            self.close()

            self.main_window = MainWindow(user_log_result)
            self.main_window.show()

    def open_reg_page(self):
        self.reg_window.show()
        self.close()

    def reset_fields(self):
        self.nickname_input_field.clear()
        self.password_input_field.clear()
