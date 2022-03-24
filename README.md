# GUI for "tesseract" OCR

 The GUI for Tesseract OCR software in Windows 64-bit platform

![](https://img.shields.io/badge/OS-Windows%2064--bit-lightgrey)
![](https://img.shields.io/badge/dependencies-tesseract--ocr%2Ftesseract-green)
![](https://img.shields.io/badge/dependencies-Python%203.9-blue)

## Introduction

This software is the graphic interface for Tesseract OCR software. When the user inputs a image by clipboard or file, the software can recognize the characters in English and Chinese and display the text on the interface.

## Acknowledgement

Tesseract OCR: https://github.com/tesseract-ocr/tesseract

## Usage

**End user**: Download from the latest release, unzip and run `gui_for_tesseract_ocr.exe`.

**Developer**:

```bash
pip install -r requirements.txt
pyinstaller gui_for_tesseract_ocr.spec
```