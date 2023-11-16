from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from settings import *
from styles import *
from database_controller import get_user_by_id, update_user


class AccountWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.user = get_user_by_id(self.user_id)

        widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle(f"Edit Account")
        self.setMaximumSize(QSize(ACCOUNT_INFO_WINDOW_WIDTH, ACCOUNT_INFO_WINDOW_HEIGHT))
        self.setMinimumSize(QSize(ACCOUNT_INFO_WINDOW_WIDTH, ACCOUNT_INFO_WINDOW_HEIGHT))

        self.label = QLabel()
        self.label.setText('EDIT ACCOUNT INFO')
        self.label.setStyleSheet(CENTERED_LABEL)
        self.label.setAlignment(Qt.AlignCenter)

        username_layout = QHBoxLayout()
        username_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        username_label = QLabel()
        username_label.setText('USERNAME')
        username_label.setStyleSheet(REG_LABEL)
        username_label.setMinimumSize(QSize(55, 20))

        self.username_input_field = QLineEdit()
        self.username_input_field.setPlaceholderText('Enter a nickname...')
        self.username_input_field.setMinimumSize(QSize(215, 20))

        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input_field)

        initials_layout = QHBoxLayout()
        initials_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        initials_label = QLabel()
        initials_label.setText('INITIALS')
        initials_label.setStyleSheet(REG_LABEL)
        initials_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        initials_label.setMinimumSize(QSize(55, 20))

        self.initials_input_field = QLineEdit()
        self.initials_input_field.setPlaceholderText('Enter initials...')
        self.initials_input_field.setMinimumSize(QSize(215, 20))

        initials_layout.addWidget(initials_label)
        initials_layout.addWidget(self.initials_input_field)

        password_label = QLabel()
        password_label.setText('PASSWORD')
        password_label.setStyleSheet(REG_LABEL)

        self.show_password = False
        self.password_input_field = QLineEdit()
        self.password_input_field.setEchoMode(QLineEdit.Password)
        self.password_input_field.setPlaceholderText('Enter your password...')
        self.password_input_field.setMinimumSize(QSize(120, 20))

        self.show_password_button = QPushButton('Toggle')
        self.show_password_button.clicked.connect(self.toggle_password)

        password_region_layout = QHBoxLayout()
        password_region_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        password_region_layout.addWidget(password_label)
        password_region_layout.addWidget(self.password_input_field)
        password_region_layout.addWidget(self.show_password_button)

        self.save_settings_button = QPushButton('Save')
        self.save_settings_button.clicked.connect(self.save_info)

        self.reset_fields_button = QPushButton('Reset Fields')
        self.reset_fields_button.clicked.connect(self.reset_fields)

        self.username_input_field.setText(self.user['nickname'])
        self.initials_input_field.setText(self.user['name'])
        self.password_input_field.setText(self.user['password'])

        layout.addWidget(self.label)

        layout.addLayout(username_layout)
        layout.addLayout(initials_layout)
        layout.addLayout(password_region_layout)

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
