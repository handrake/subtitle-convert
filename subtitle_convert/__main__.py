import sys

from PyQt5.QtWidgets import QApplication

try:
    from .subtitle_convert_gui import SubtitleConvertMainDialog
except ImportError:
    from subtitle_convert.subtitle_convert_gui import SubtitleConvertMainDialog

if __name__ == "__main__":
    APP = QApplication(sys.argv)
    DIALOG = SubtitleConvertMainDialog()
    DIALOG.show()
    APP.exec_()
