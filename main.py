from Windows.RegisterWindow import RegisterWindow
from PyQt5.QtWidgets import *

import sys


app = QApplication(sys.argv)
login_register_window = RegisterWindow()

sys.exit(app.exec())
