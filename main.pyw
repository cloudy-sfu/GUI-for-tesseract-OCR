import os
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import tesserocr
from ocr_wrapper import BatchOCR, SingleOCR, ClipboardOCR, pixmap_to_pillow_image


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__(flags=Qt.Window)
        dpi = self.screen().logicalDotsPerInch() / 96
        font_size = 14 if dpi <= 1 else (12 if 1 < dpi <= 1.25 else (10 if 1.25 < dpi <= 1.5 else 8))
        self.setStyleSheet(f'font-family: "Microsoft YaHei", Calibri, Ubuntu; font-size: {font_size}pt;')
        self.resize(1280, 720)
        self.setWindowTitle('Chinese and English OCR')
        self.center()

        os.makedirs('raw/', exist_ok=True)
        os.makedirs('raw/models', exist_ok=True)
        self.operator = None
        self.busy = False
        self.project_root = os.path.abspath('raw/')
        self.lang = 'eng'

        self.create_menu_bar()
        self.create_language_box()
        self.target_displayed = QLabel(self)
        self.target_displayed.setText(self.project_root)
        self.source_displayed = QLabel(self)
        self.lang_displayed = QLabel(self)
        self.lang_displayed.setText(self.lang)
        self.pbar = QProgressBar(self)
        self.message = QTextEdit(self)

        main_part = QWidget(self)
        main_layout = QFormLayout(main_part)
        main_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        main_layout.addRow('Source:', self.source_displayed)
        main_layout.addRow('Target:', self.target_displayed)
        main_layout.addRow('Language:', self.lang_displayed)
        main_layout.addRow('Progress:', self.pbar)
        main_layout.addRow('Message:', self.message)
        self.setCentralWidget(main_part)

        self.status = QStatusBar()
        self.status.showMessage('Ready.', 0)
        self.setStatusBar(self.status)

    def create_menu_bar(self):
        # File menu
        open_project_root = QAction('&Open target folder ...', self)
        open_project_root.triggered.connect(self.open_project_root)
        open_project_root.setShortcut('Ctrl+T')
        open_pretrained_models_repo = QAction('&Download pretrained language modules ...', self)
        open_pretrained_models_repo.triggered.connect(self.download_pretrained_models)
        open_pretrained_models_path = QAction("O&pen language modules ...", self)
        open_pretrained_models_path.triggered.connect(self.open_pretrained_models)
        switch_language = QAction('&Switch language ...', self)
        switch_language.triggered.connect(self.switch_language)
        switch_language.setShortcut('Ctrl+L')
        close = QAction('&Exit', self)
        close.triggered.connect(self.close)
        close.setShortcut('Ctrl+W')
        # Recognize menu
        reco_folder = QAction('From &folder ...', self)
        reco_folder.triggered.connect(self.ocr_batch)
        reco_file = QAction('From &single image ...', self)
        reco_file.triggered.connect(self.ocr_single)
        reco_clipboard = QAction('From &clipboard', self)
        reco_clipboard.triggered.connect(self.ocr_clipboard)
        reco_clipboard.setShortcut('Ctrl+Shift+V')
        # About menu
        version = QAction('&Version and supported language', self)
        version.triggered.connect(self.print_version)
        # First-level buttons
        file = QMenu('&File', self)
        file.addActions([open_project_root, open_pretrained_models_repo, open_pretrained_models_path,
                         switch_language, close])
        recognize = QMenu('&Recognize', self)
        recognize.addActions([reco_folder, reco_file, reco_clipboard])
        help_center = QMenu('&Help', self)
        help_center.addActions([version])
        # Menu bar
        menubar = QMenuBar()
        menubar.addMenu(file)
        menubar.addMenu(recognize)
        menubar.addMenu(help_center)
        self.setMenuBar(menubar)

    def status_check_decorator(action_name, *args, **kwargs):
        def status_check_decorator_1(pyfunc):
            def status_check(self):
                if not self.busy:
                    self.busy = True
                    self.status.showMessage(f'{action_name} ...', 0)
                    self.message.clear()
                    pyfunc(self, *args, **kwargs)
                    self.busy = False
                    self.status.showMessage('Ready.', 0)
                else:
                    self.status.showMessage('The program is busy ...', 0)

            return status_check

        return status_check_decorator_1

    def delayed_thread_check_decorator(action_name, *args, **kwargs):
        def delayed_thread_check_decorator_1(pyfunc):
            def delayed_thread_check(self):
                if not self.busy:
                    self.busy = True
                    self.status.showMessage(f'{action_name} ...', 0)
                    self.message.clear()
                    pyfunc(self, *args, **kwargs)
                else:
                    self.status.showMessage('The program is busy ...', 0)

            return delayed_thread_check

        return delayed_thread_check_decorator_1

    @delayed_thread_check_decorator(action_name='Recognize folder')
    def ocr_batch(self):
        fp = QFileDialog.getExistingDirectory(self, caption='Images to recognize', options=QFileDialog.ShowDirsOnly)
        if not (fp and os.path.isdir(fp)):
            self.message.append('The source to recognize does not exist.')
            self.delayed_thread_finished()
            return
        dist = QFileDialog.getExistingDirectory(self, caption='Export to', options=QFileDialog.ShowDirsOnly)
        os.makedirs(dist, exist_ok=True)
        self.project_root = dist
        self.source_displayed.setText(fp)
        self.operator = BatchOCR(fp, dist, self.lang)
        self.operator.start()
        self.operator.progress.connect(self.pbar.setValue)
        self.operator.gui_message.connect(self.message.append)
        self.operator.done.connect(self.delayed_thread_finished)

    @delayed_thread_check_decorator(action_name='Recognize from clipboard')
    def ocr_clipboard(self):
        clipboard = QApplication.clipboard()
        pixmap = clipboard.pixmap()
        image = pixmap_to_pillow_image(pixmap)
        if not image:
            self.message.append('There is no picture in the clipboard.')
            self.delayed_thread_finished()
            return
        self.source_displayed.setText('Clipboard')
        self.operator = ClipboardOCR(image, self.lang)
        self.operator.start()
        self.operator.progress.connect(self.pbar.setValue)
        self.operator.gui_message.connect(self.message.append)
        self.operator.done.connect(self.delayed_thread_finished)

    @delayed_thread_check_decorator(action_name='OCR for single image')
    def ocr_single(self):
        fp, _ = QFileDialog.getOpenFileName(self, filter='Images (*.png *.jpeg *.jpg)')
        if not (fp and os.path.isfile(fp)):
            self.message.append('The image to recognize does not exist.')
            self.delayed_thread_finished()
            return
        self.source_displayed.setText(fp)
        self.operator = SingleOCR(fp, self.lang)
        self.operator.start()
        self.operator.progress.connect(self.pbar.setValue)
        self.operator.gui_message.connect(self.message.append)
        self.operator.done.connect(self.delayed_thread_finished)

    @status_check_decorator(action_name='Open target folder')
    def open_project_root(self):
        if not os.path.exists(self.project_root):
            self.message.append('The target folder does not exist.')
        q_url = QUrl()
        QDesktopServices.openUrl(q_url.fromLocalFile(self.project_root))

    def delayed_thread_finished(self, *args):
        self.busy = False
        self.status.showMessage('Ready.', 0)

    def center(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    @status_check_decorator(action_name='print_version')
    def print_version(self):
        lib, language = tesserocr.get_languages('raw/models/')
        lib = os.path.abspath(lib)
        version = tesserocr.tesseract_version()
        self.message.clear()
        self.message.append(f'Tesseract version: {version}')
        self.message.append(f'Pretrained language models: {lib}')
        self.message.append(f'Supported language: {language}')

    @status_check_decorator(action_name='download_pretrained_models')
    def download_pretrained_models(self):
        # https://stackoverflow.com/questions/3684857/pyqt4-open-website-in-standard-browser-on-button-click
        libpath = QUrl('https://github.com/tesseract-ocr/tessdata/tree/4767ea922bcc460e70b87b1d303ebdfed0897da8')
        QDesktopServices().openUrl(libpath)

    @status_check_decorator(action_name='open_pretrained_models')
    def open_pretrained_models(self):
        libpath = QUrl().fromLocalFile('raw/models')
        QDesktopServices().openUrl(libpath)

    def create_language_box(self):
        _, languages = tesserocr.get_languages('raw/models/')
        self.language_combo = QComboBox()
        self.language_combo.addItems(languages)
        self.language_box = QDialog()
        dpi = self.screen().logicalDotsPerInch() / 96
        font_size = 14 if dpi <= 1 else (12 if 1 < dpi <= 1.25 else (10 if 1.25 < dpi <= 1.5 else 8))
        self.language_box.setStyleSheet(f'font-family: "Microsoft YaHei", Calibri, Ubuntu; font-size: {font_size}pt;')
        self.language_box.setMinimumWidth(480)
        self.language_box.setWindowTitle('Select a language')
        layout = QVBoxLayout()
        hint = QLabel('Please select a supported language. If your language is not supported, please '
                      'follow the guidance at https://github.com/cloudy-sfu/GUI-for-tesseract-OCR and '
                      'import your first language model.')
        hint.setWordWrap(True)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.language_box.accept)
        button_box.rejected.connect(self.language_box.reject)
        layout.addWidget(hint)
        layout.addWidget(self.language_combo)
        layout.addWidget(button_box)
        self.language_box.setLayout(layout)

    @status_check_decorator(action_name='switch_language')
    def switch_language(self):
        action = self.language_box.exec_()
        if action == QDialog.Accepted:
            self.lang = self.language_combo.currentText()
            self.lang_displayed.setText(self.lang)

    # Deceive IDE grammar warning; must be written end of the class.
    status_check_decorator = staticmethod(status_check_decorator)
    delayed_thread_check_decorator = staticmethod(delayed_thread_check_decorator)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myw = MyWindow()
    myw.show()
    sys.exit(app.exec_())
