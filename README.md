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

### 1. Developers

1. Compile from source code and embed it at the Python project directory. In this case, you should modify `get_ocr_path` and set Tesseract installation path as the current directory.
2. Run `pip install -r requirements.txt`.
3. Run `main.pyw`.

### 2. Ordinary users

1. Download Tesseract for Windows at [this webpage](https://digi.bib.uni-mannheim.de/tesseract/) and install it, following the guidance of setup program.
2. Get the latest release of this software and run `main.exe`.
