import tesserocr
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage
import os


class BatchOCR(QThread):
    progress = pyqtSignal(int, name='progress')
    gui_message = pyqtSignal(str, name='error_message')
    done = pyqtSignal(bool, name='done')

    def __init__(self, input_folder, output_folder, lang):
        super(BatchOCR, self).__init__()
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.lang = lang

    def run(self) -> None:
        # get files' path
        filenames = []
        for parent, _, files in os.walk(self.input_folder):
            filenames += [(parent, x) for x in files if os.path.splitext(x)[1].lower() in ['.jpg', '.png']]
        n_files = len(filenames)
        if n_files == 0:
            self.gui_message.emit('This folder does not contains any picture.')
            self.done.emit(True)
            return
        # OCR
        for i, (parent, name) in zip(range(n_files), filenames):
            filepath = os.path.join(parent, name)
            output_image_name, output_image_ext = os.path.splitext(name)
            output_path_text = os.path.join(self.output_folder, output_image_name + '.txt')
            try:
                text = tesserocr.file_to_text(filepath, oem=tesserocr.OEM.TESSERACT_ONLY, path='raw/models',
                                              lang=self.lang)
            except Exception as e:
                self.gui_message.emit(f'{filepath} - {e}')
                self.gui_message.emit('Maybe you have not imported a language model. Please follow the usage at '
                                      'https://github.com/cloudy-sfu/GUI-for-tesseract-OCR and import your first '
                                      'language model.')
                self.progress.emit((i + 1, n_files))
                continue
            if not text:
                self.gui_message.emit(f'{filepath} doesn\'t contain text.')
            with open(output_path_text, 'w') as f:
                f.write(text)
            del text
            progress_percentage = int((i + 1) / n_files * 100)
            self.progress.emit(progress_percentage)
        self.gui_message.emit('Click "File | Open target folder" in menu bar to view the exported images.')
        self.done.emit(True)


class SingleOCR(QThread):
    progress = pyqtSignal(int, name='progress')
    gui_message = pyqtSignal(str, name='gui_message')
    done = pyqtSignal(bool, name='done')

    def __init__(self, input_file, lang):
        super(SingleOCR, self).__init__()
        self.input_file = input_file
        self.lang = lang

    def run(self) -> None:
        try:
            text = tesserocr.file_to_text(self.input_file, oem=tesserocr.OEM.TESSERACT_ONLY, path='raw/models',
                                          lang=self.lang)
        except Exception as e:
            self.gui_message.emit(f'{self.input_file} - {e}')
            self.gui_message.emit('Maybe you have not imported a language model. Please follow the usage at '
                                  'https://github.com/cloudy-sfu/GUI-for-tesseract-OCR and import your first language '
                                  'model.')
            self.done.emit(True)
            return
        self.gui_message.emit(text)
        del text
        self.progress.emit(100)
        self.done.emit(True)


def pixmap_to_pillow_image(pixmap):
    q_image = pixmap.toImage()
    q_image = q_image.convertToFormat(QImage.Format_RGBA8888)
    width = q_image.width()
    height = q_image.height()
    if q_image.bits() is None:
        return
    buffer = q_image.bits().asarray(q_image.byteCount())
    pillow_image = Image.frombytes("RGBA", (width, height), buffer, "raw", "BGRA")
    return pillow_image


class ClipboardOCR(QThread):
    progress = pyqtSignal(int, name='progress')
    gui_message = pyqtSignal(str, name='gui_message')
    done = pyqtSignal(bool, name='done')

    def __init__(self, pillow_image, lang):
        super(ClipboardOCR, self).__init__()
        self.pillow_image = pillow_image
        self.lang = lang

    def run(self) -> None:
        try:
            text = tesserocr.image_to_text(self.pillow_image, oem=tesserocr.OEM.TESSERACT_ONLY, path='raw/models',
                                           lang=self.lang)
        except Exception as e:
            self.gui_message.emit(e.__str__())
            self.gui_message.emit('Maybe you have not imported a language model. Please follow the usage at '
                                  'https://github.com/cloudy-sfu/GUI-for-tesseract-OCR and import your first language '
                                  'model.')
            self.done.emit(True)
            return
        self.gui_message.emit(text)
        del text
        self.progress.emit(100)
        self.done.emit(True)
