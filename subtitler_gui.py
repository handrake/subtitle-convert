import sys
import os

from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QListWidgetItem, QAbstractItemView,QMessageBox

class SubtitlerMainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "main_gui.ui"), self)

        self.input_file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.add_file_button.released.connect(self._select_input_file)
        self.delete_all_button.released.connect(self._delete_all_input_files)
        self.delete_button.released.connect(self._delete_input_files)

        self.output_folder_edit.setText(os.path.expanduser('~'))
        self.browse_output_folder_button.released.connect(self._select_output_folder)

    def _select_input_file(self):
        file_names, _ = QFileDialog.getOpenFileNames(directory=os.path.expanduser('~'))
        self.input_file_list.addItems(file_names)

    def _delete_all_input_files(self):
        self.input_file_list.clear()

    def _delete_input_files(self):
        for selectedItem in self.input_file_list.selectedItems():
            self.input_file_list.takeItem(self.input_file_list.row(selectedItem))

    def _select_output_folder(self):
        folder_name = QFileDialog.getExistingDirectory(directory=os.path.expanduser('~'),
                                                       options=QFileDialog.ShowDirsOnly)
        if not os.path.exists(folder_name):
            QMessageBox.Information("폴더가 없습니다")
        else:
            self.output_folder_edit.setText(folder_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SubtitlerMainDialog()
    dialog.show()
    app.exec_()
