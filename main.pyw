from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys
import subprocess


def get_ocr_path():
    try:
        with open('tesseracts_path', 'r') as f:
            configured_path = f.read()
    except FileNotFoundError:
        with open('tesseracts_path', 'w') as _:
            pass
        configured_path = ''
    ocr_path = [
        configured_path,
        os.path.join(r'C:\Users', os.environ['USERNAME'], r'AppData\Local\Tesseract-OCR'),
        r'C:\Program Files (x86)\Tesseract-OCR',
    ]
    for location in ocr_path:
        if os.path.isdir(location):
            return location
    return None


class MyWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        dpi = self.screen().logicalDotsPerInch() / 96
        font_size = 14 if dpi <= 1 else (11 if 1 < dpi <= 1.25 else (9 if 1.25 < dpi <= 1.5 else 8))
        self.setFont(QFont("Calibri", font_size))
        self.resize(800, 480)
        self.setWindowTitle("OCR (win64) GUI for Tesseract")
        self.center()

        self.base_dir = get_ocr_path()

        self.label1 = QLabel(self)
        self.label1.setText("Tesseract installed at:")
        self.label1.move(10, 10)

        self.box1 = QLineEdit(self)
        self.box1.move(180, 10)
        self.box1.resize(400, 25)
        self.box1.setText(self.base_dir)

        self.button1 = QToolButton(self)
        self.button1.move(600, 10)
        self.button1.setText("Change")
        self.button1.clicked.connect(self.change_path)

        self.box2 = QLabel(self)
        self.box2.move(10, 50)
        self.box2.resize(385, 380)

        self.box3 = QTextEdit(self)
        self.box3.move(405, 50)
        self.box3.resize(385, 380)
        self.box3.setText('Ready.')

        self.button2 = QToolButton(self)
        self.button2.move(10, 440)
        self.button2.setText('Get image from clipboard')
        self.button2.clicked.connect(self.paste_picture)

        self.button3 = QToolButton(self)
        self.button3.move(220, 440)
        self.button3.setText('Get image from file')
        self.button3.clicked.connect(self.read_picture)

        self.label2 = QLabel(self)
        self.label2.move(405, 440)
        self.label2.setText('Select language:')

        self.box4 = QComboBox(self)
        self.box4.move(530, 440)
        self.box4.resize(130, 25)
        try:
            for file in os.listdir(os.path.join(self.base_dir, 'tessdata')):
                filename, extension = os.path.splitext(file)
                if extension == '.traineddata':
                    self.box4.addItem(filename)
        except Exception as e:
            self.box3.setText(f'Error: {e}')

        self.button4 = QToolButton(self)
        self.button4.move(680, 440)
        self.button4.setText('Run OCR')
        self.button4.clicked.connect(self.ocr)

        self.ocr_runtime = None

    def center(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def change_path(self):
        self.box3.setText('Waiting: change tesseract\'s installation directory.')
        fp = QFileDialog.getExistingDirectory(self)
        with open('tesseracts_path', 'w') as f:
            f.write(fp)
        self.box1.setText(fp)
        self.box3.setText('Ready.')

    def paste_picture(self):
        self.box3.setText('Waiting: Read image from clipboard.')
        clipboard = QApplication.clipboard()
        picture = clipboard.pixmap()
        picture.save('clipboard.png')
        self.box2.setPixmap(picture.scaled(385, 380))
        self.box3.setText('Ready.')

    def read_picture(self):
        self.box3.setText('Waiting: Read image from file.')
        fp, _ = QFileDialog.getOpenFileName(self, filter='Images (*.png *.jpeg *.jpg *.bmp)')
        picture = QPixmap(fp)
        picture.save('clipboard.png')
        self.box2.setPixmap(picture.scaled(385, 380))
        self.box3.setText('Ready.')

    def ocr(self):
        self.box3.setText('Waiting: Execute OCR.')
        self.ocr_runtime = OCR(base_dir=self.base_dir, language_code=self.box4.currentText())
        self.ocr_runtime.start()
        self.ocr_runtime.signal1.connect(self.box3.setText)


class OCR(QThread):
    signal1 = pyqtSignal(str)

    def __init__(self, base_dir, language_code):
        super(OCR, self).__init__()
        self.base_dir = base_dir
        self.language_code = language_code

    def run(self):
        try:
            command = rf'{self.base_dir}\tesseract.exe clipboard.png clipboard -l {self.language_code}'
            action = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      stdin=subprocess.DEVNULL)
            runtime_message = action.stdout.read().decode('utf-8')
            if 'No such file or directory' in runtime_message:
                self.signal1.emit(runtime_message)
            else:
                with open('clipboard.txt', 'r', encoding='utf-8') as f:
                    self.signal1.emit(f.read())
        except Exception as e:
            self.signal1.emit(f'Error: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myw = MyWindow()
    myw.show()
    sys.exit(app.exec_())
