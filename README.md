# GUI for "tesseract" OCR

 The GUI for Tesseract OCR software in Windows 64-bit platform

![](https://img.shields.io/badge/OS-Windows%2010%2064--bit-lightgrey)
![](https://img.shields.io/badge/dependencies-Python%203.10-blue)

## Usage

1. Unzip and click `GUI-for-tesseract-OCR.exe` to run this program.
2. By default, we provide English language model in the installation package. Click `Help | Version and supported language ` to find which language models have been installed.
    ![image-20230212142100249](./assets/image-20230212142100249.png)

If the languages you want is not supported: 

3.   Click `File | Download pretrained language models ` to find the language models. The program will call your default web browser and direct you to the download page.
     ![image-20230212142123835](./assets/image-20230212142123835.png)
4.   Refer to [Language code](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html) to know which file you should download.
5.   Click the file name.
     ![image-20230212141930496](./assets/image-20230212141930496.png)
6.   Click the download button, waiting the web browser to download this file.
     ![image-20230212142409014](./assets/image-20230212142409014.png)
7.   Click `File | Open language modules`. Then, the program will automatically call the file explorer and pop up a folder. Move the file you downloaded to the popped-up folder. Finally, close the file explorer.
     ![image-20230212142444241](./assets/image-20230212142444241.png)
8.   If you want to switch the language, which OCR program uses, please click `File | Switch language` . In the popped-up dialog "Select a language", choose your language and click "OK".
     ![image-20230212142823934](./assets/image-20230212142823934.png)
     The current language will appear in the "Language" row in the main window.

Now, you're set up and can choose any item in `Recognize` menu to start an OCR task.

![image-20230212143110006](./assets/image-20230212143110006.png)

## Acknowledgement

The files in `raw/models` are copied from [Tessdata](https://github.com/tesseract-ocr/tessdata/tree/4767ea922bcc460e70b87b1d303ebdfed0897da8) which is not included in the license of this repository. The copyright is reserved by Tessdata, and we redistribute these files based on their license.

