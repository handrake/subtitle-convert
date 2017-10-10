import sys

from PyQt5.QtWidgets import QApplication

from subtitle_convert.subtitle_convert_gui import SubtitleConvertMainWindow

if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WIN = SubtitleConvertMainWindow()
    WIN.show()
    sys.exit(APP.exec_())
