import sys
import os

from PyQt5 import QtCore, uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QListWidgetItem, QAbstractItemView,QMessageBox

SUPPORTED_FILE_TYPES = ["smi", "srt", "txt"]

class SubtitlerWorkerThread(QThread):
    signal = QtCore.pyqtSignal(int)

    def __init__(self, input_files, output_folder, output_type, overwrite_on = False):
        QThread.__init__(self)
        self.input_files = input_files
        self.output_folder = output_folder
        self.output_type = output_type
        self.overwrite_on = overwrite_on

    def run(self):
        self.signal.emit(0)

class SubtitlerMainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "main_gui.ui"), self)

        self.input_file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.input_folder = os.path.expanduser('~')

        self.add_file_button.released.connect(self._select_input_file)
        self.delete_all_button.released.connect(self._delete_all_input_files)
        self.delete_button.released.connect(self._delete_input_files)

        self.output_folder_edit.setText(os.path.expanduser('~'))
        self.output_folder_edit.returnPressed.connect(self._handle_folder_input)
        self.output_type_combo.currentIndexChanged.connect(self._update_output_type)
        self.output_type_combo.insertItems(0, SUPPORTED_FILE_TYPES)
        self.output_type = self.output_type_combo.currentText()

        self.browse_output_folder_button.released.connect(self._select_output_folder)

        self.convert_button.released.connect(self.process_conversion)

        self.output_folder = os.path.expanduser('~')

    def _select_input_file(self):
        file_names, _ = QFileDialog.getOpenFileNames(directory=self.input_folder)
        if file_names:
            self.input_folder = os.path.dirname(file_names[0])
        self.input_file_list.addItems(file_names)

    def _delete_all_input_files(self):
        self.input_file_list.clear()

    def _delete_input_files(self):
        for selectedItem in self.input_file_list.selectedItems():
            self.input_file_list.takeItem(self.input_file_list.row(selectedItem))

    def _handle_folder_input(self):
        folder_name = self.output_folder_edit.text()
        if not os.path.exists(folder_name):
            QMessageBox.information(self, "Error", "폴더가 없습니다")
            self.output_folder_edit.setText(self.output_folder)
        else:
            self.output_folder = folder_name

    def _set_output_folder(self, folder_name):
        self.output_folder = folder_name
        self.output_folder_edit.setText(folder_name)

    def _select_output_folder(self):
        folder_name = QFileDialog.getExistingDirectory(directory=self.output_folder,
                                                       options=QFileDialog.ShowDirsOnly)
        self._set_output_folder(folder_name)

    def _update_output_type(self):
        self.output_type = SUPPORTED_FILE_TYPES[self.output_type_combo.currentIndex()]

    def _validate_inputs(self):
        to_be_deleted = []
        for i in range(self.input_file_list.count()):
            file = self.input_file_list.item(i).text()
            file_type = os.path.splitext(file)[1].lower()[1:]
            if (not os.path.exists(file) or file_type == self.output_type
                or file_type == "txt" or file_type not in SUPPORTED_FILE_TYPES):
                to_be_deleted.append(self.input_file_list.item(i))

        for item in to_be_deleted:
            self.input_file_list.takeItem(self.input_file_list.row(item))

    def process_conversion(self):
        self._validate_inputs()
        self.worker_thread = SubtitlerWorkerThread([str(self.input_file_list.item(i).text())
                                                   for i in range(self.input_file_list.count())],
                                                   self.output_type, self.output_folder, True)
        self.worker_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SubtitlerMainDialog()
    dialog.show()
    app.exec_()
