import sys

from PyQt5.QtWidgets import QApplication
from .subtitle_convert_gui import SubtitleConvertMainDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SubtitleConvertMainDialog()
    dialog.show()
    app.exec_()
