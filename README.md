# OCR (win64) GUI for Tesseract
 The GUI for Tesseract OCR software in Windows 64-bit platform

![](https://img.shields.io/badge/OS-Windows%2064--bit-lightgrey)
![](https://img.shields.io/badge/dependencies-tesseract--ocr%2Ftesseract-green)
![](https://img.shields.io/badge/dependencies-Python%203.9-blue)

# Acknowledge

[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

# Install

For developers:

1. Compile from source code and embed it at the Python project directory. 
   In this case, you should modify `get_ocr_path` and set Tesseract installation
   path as the current directory.
2. Run 
   ```
   pip install -r requirements.txt
   ```
3. Run `main.pyw`.

For users:

1. Download Tesseract for Windows at [this webpage](https://digi.bib.uni-mannheim.de/tesseract/)
   and install it, following the guidance of setup program.
2. Get the latest release and run `main.exe`.
