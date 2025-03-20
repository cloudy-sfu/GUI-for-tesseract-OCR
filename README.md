# GUI for "tesseract" OCR

 The GUI for Tesseract OCR software in Windows 64-bit platform

![](https://img.shields.io/badge/OS-Windows%2010%2064--bit-navy)
![](https://img.shields.io/badge/dependencies-Python%203.12-blue)

## Install

From release:

1. Unzip and click `GUI-for-tesseract-OCR.exe` to run this program.

From source code:

1. Create a Python 3.12 virtual environment.

2. Set the program's root directory as the current folder.

3. Run the following commands.
    ```
    pip install -r requirements.txt
    ```

4. (Optional) To compile to an executable file, run the following command.
    ```
    python solve_msvcp140_conflict.py
    pyinstaller main.spec
    ```

> [!NOTE]
>
> Not Windows 10 64-bit, Python 3.12?
>
> Before starting step 3, go to https://github.com/simonflueckiger/tesserocr-windows_build/releases and download corresponding Tesseract package, and delete `tesserocr` line in `requirements.txt`.

## Usage

1. By default, we provide an English language model in the installation package. Click `Help | Version and supported language ` to find installed language models.
    ![image-20230212142100249](./assets/image-20230212142100249.png)

If the languages you want are not supported:

3.   Click `File | Download pretrained language models ` to find the language models. The program will call your default web browser and direct you to the download page.
     ![image-20230212142123835](./assets/image-20230212142123835.png)
4.   Refer to [Language code](https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html) to know which file you should download.
5.   Click the file name.
     ![image-20230212141930496](./assets/image-20230212141930496.png)
6.   Click the download button, waiting the web browser to download this file.
     ![image-20230212142409014](./assets/image-20230212142409014.png)
7.   Click `File | Open language modules`. Then, the program will automatically call the file explorer and pop up a folder. Move the file you downloaded to the popped-up folder. Finally, close the file explorer.
     ![image-20230212142444241](./assets/image-20230212142444241.png)
8.   If you want to switch the language, that the OCR program uses, please click `File | Switch language` . In the popped-up dialog "Select a language", choose your language and click "OK".
     ![image-20230212142823934](./assets/image-20230212142823934.png)
     The current language will appear in the "Language" row in the main window.
9.   Now, you're set up and can choose any item in `Recognize` menu to start an OCR task.![image-20230212143110006](./assets/image-20230212143110006.png)

## Acknowledgment

[Tessdata](https://github.com/tesseract-ocr/tessdata/tree/4767ea922bcc460e70b87b1d303ebdfed0897da8) for pretrained models

[Tesserocr Windows build](https://github.com/simonflueckiger/tesserocr-windows_build)
