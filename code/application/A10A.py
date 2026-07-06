# UFT-8
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from PyQt5.QtWidgets import *
from ui.korisnicko_sucelje import Sucelje



if __name__=='__main__':

    app = QApplication(sys.argv)
    window = Sucelje()
    sys.exit(app.exec())
    