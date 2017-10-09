import sys
import os

from PyQt5 import QtCore, uic
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QListWidgetItem, QAbstractItemView,QMessageBox

from samitizer import Smi

SUPPORTED_INPUT_TYPES = ["smi"]
SUPPORTED_OUTPUT_TYPES = ["srt", "txt"]

SUPPORTED_OUTPUT_ENCODING = ["utf8", "cp949"]

class SubtitlerWorkerThread(QThread):
    log_signal = QtCore.pyqtSignal(str)

    def __init__(self, input_files, output_folder, output_type, output_encoding, overwrite_on = False):
        QThread.__init__(self)
        self.input_files = input_files
        self.output_folder = output_folder
        self.output_type = output_type
        self.output_encoding = output_encoding
        self.overwrite_on = overwrite_on

    def run(self):
        for input_file in self.input_files:
            input_file_name = os.path.basename(input_file)
            input_type = os.path.splitext(input_file)[1].lower()[1:]
            output_file = os.path.join(self.output_folder,
                                       os.path.splitext(input_file_name)[0] + '.' + self.output_type)
            output_file_name = os.path.basename(output_file)
            if os.path.exists(output_file) and not self.overwrite_on:
                self.log.signal.emit("{}을 건너뜁니다...".format(input_file_name))
                continue
            self.log_signal.emit("{}을 읽습니다...".format(input_file_name))

            with open(output_file, 'w', encoding=self.output_encoding) as file_out:
                if input_type == "smi":
                    smi = Smi(input_file)
                    try:
                        if self.output_type == "srt":
                            file_out.write(smi.convert('srt', lang='KRCC'))
                        elif self.output_type == "txt":
                            file_out.write(smi.convert('plain', lang='KRCC'))
                        self.log_signal.emit("{}으로 변환했습니다".format(output_file_name))
                    except:
                        self.log_signal.emit("<b>{}을 변환하지 못했습니다</b>".format(input_file_name))


class SubtitlerProcessDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "process_gui.ui"), self)

        self.ok_button.released.connect(self.close)

    def update_log_text(self, line):
        self.log_text_browser.append(line)

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
        self.output_type_combo.insertItems(0, SUPPORTED_OUTPUT_TYPES)
        self.output_type = self.output_type_combo.currentText()

        self.output_encoding_combo.currentIndexChanged.connect(self._update_output_encoding)
        self.output_encoding_combo.insertItems(0, SUPPORTED_OUTPUT_ENCODING)
        self.output_encoding = self.output_encoding_combo.currentText()

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
        self.output_type = SUPPORTED_OUTPUT_TYPES[self.output_type_combo.currentIndex()]

    def _update_output_encoding(self):
        self.output_encoding = SUPPORTED_OUTPUT_ENCODING[self.output_encoding_combo.currentIndex()]

    def _validate_inputs(self):
        to_be_deleted = []
        for i in range(self.input_file_list.count()):
            file = self.input_file_list.item(i).text()
            file_type = os.path.splitext(file)[1].lower()[1:]
            if (not os.path.exists(file) or file_type == self.output_type
                or file_type not in SUPPORTED_INPUT_TYPES):
                to_be_deleted.append(self.input_file_list.item(i))

        for item in to_be_deleted:
            self.input_file_list.takeItem(self.input_file_list.row(item))

    def process_conversion(self):
        self._validate_inputs()

        if self.input_file_list.count() == 0:
            QMessageBox.information(self, "", "변환할 파일이 없습니다")
            return

        self.process_dialog = SubtitlerProcessDialog()

        self.worker_thread = SubtitlerWorkerThread([str(self.input_file_list.item(i).text())
                                                   for i in range(self.input_file_list.count())],
                                                   self.output_folder, self.output_type,
                                                   self.output_encoding, True)

        self.worker_thread.log_signal.connect(self.process_dialog.update_log_text)
        self.worker_thread.start()
        self.process_dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = SubtitlerMainDialog()
    dialog.show()
    app.exec_()
