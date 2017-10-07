import sys
import os

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QDialog, QApplication

class SubtitlerMainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "main_gui.ui"), self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SubtitlerMainDialog()
    dialog.show()
    app.exec_()
