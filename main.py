import json
import os
import subprocess

import pywebio

if os.path.exists('./config.json'):
    with open('./config.json', 'r') as f_config:
        config = json.load(f_config)
    if not (
        isinstance(config, dict) and
        'language' in config.keys() and
        isinstance(config.get('language'), list) and
        'installed_path' in config.keys() and
        isinstance(config.get('installed_path'), str)
    ):
        config = {'language': [], 'installed_path': ''}
else:
    config = {'language': [], 'installed_path': ''}
if not os.path.isdir(config['installed_path']):
    ocr_path = [r'C:\Program Files (x86)\Tesseract-OCR', r'C:\Program Files\Tesseract-OCR']
    if 'USERNAME' in os.environ.keys():
        ocr_path.append(os.path.join(r'C:\Users', os.environ['USERNAME'], r'AppData\Local\Tesseract-OCR'))
    for location in ocr_path:
        if os.path.isdir(location):
            config['installed_path'] = location
            break
if os.path.isdir(config['installed_path']):
    for file in os.listdir(os.path.join(config['installed_path'], 'tessdata')):
        filename, extension = os.path.splitext(file)
        if extension == '.traineddata':
            config['language'].append(filename)


def change_path():
    pywebio.output.put_markdown('[Back](/?app=index) to the index page.')
    tesseract = pywebio.input.input(label='"Tesseract OCR" installed at')
    if os.path.isdir(tesseract):
        config['installed_path'] = tesseract
        for file_ in os.listdir(os.path.join(config['installed_path'], 'tessdata')):
            filename_, extension_ = os.path.splitext(file_)
            if extension_ == '.traineddata':
                config['language'].append(filename_)
        with open('./config.json', 'w') as f:
            json.dump(config, f)
        pywebio.output.put_text('Successfully find "Tesseract OCR" here.')
    else:
        pywebio.output.put_text('Cannot find "Tesseract OCR" here.')


def index():
    pywebio.output.put_markdown(f"""
        # GUI for "Tesseract OCR"
        
        Authored by [cloudy-sfu](https://github.com/cloudy-sfu/) in 2022.
        
        ## Installation
        
        "Tesseract OCR" installed at
        ```
        {config['installed_path']}
        ```
        <center><a href="/?app=change_path">Change</a></center>
        
        ## OCR workspace
        
        Please keep patient when waiting for the OCR result.
    """)

    if config['language'] and config['installed_path'] and os.path.isdir(config['installed_path']):
        data = pywebio.input.input_group('OCR', [
            pywebio.input.file_upload('Upload the image', name='image'),
            # https://pywebio.readthedocs.io/en/latest/input.html?highlight=select#pywebio.input.select
            pywebio.input.select('Language', options=[
                (x, x) for x in config['language'] if isinstance(x, str)
            ], name='lang')
        ])
        image = data['image']['content']
        with open('./image.png', 'wb') as f:
            f.write(image)
        command = rf'"{config["installed_path"]}\tesseract.exe" image.png clipboard -l {data["lang"]}'
        action = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  stdin=subprocess.DEVNULL)
        runtime_message = action.stdout.read().decode('utf-8')
        if 'No such file or directory' in runtime_message:
            pywebio.output.put_error(runtime_message)
        else:
            with open('clipboard.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            pywebio.output.put_success(content)
    else:
        pywebio.output.put_markdown('Cannot find "Tesseract OCR" or supported language, please assign a installed'
                                    'place by "Change" link above.')


if __name__ == '__main__':
    # Debug
    # pywebio.start_server([index, change_path], auto_open_webbrowser=False, port=5000)
    # Deploy
    pywebio.start_server([index, change_path], auto_open_webbrowser=True)
