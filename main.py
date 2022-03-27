import json
import os
import subprocess

import pywebio


def _change_path(config_, user_assigned_path=None):
    ocr_path = [r'C:\Program Files (x86)\Tesseract-OCR', r'C:\Program Files\Tesseract-OCR']
    if 'USERNAME' in os.environ.keys():
        ocr_path.append(os.path.join(r'C:\Users', os.environ['USERNAME'], r'AppData\Local\Tesseract-OCR'))
    if user_assigned_path is not None:
        ocr_path.append(user_assigned_path)
    for location in ocr_path:
        if os.path.isdir(location):
            config_['installed_path'] = location
            for file in os.listdir(os.path.join(location, 'tessdata')):
                filename, extension = os.path.splitext(file)
                if extension == '.traineddata':
                    config_['language'].append(filename)
            break
    return config_


config = {'installed_path': '', 'language': []}
if os.path.exists('./config.json'):
    with open('./config.json', 'r') as f_config:
        config = json.load(f_config)
if not (
    isinstance(config, dict) and
    'language' in config.keys() and
    isinstance(config.get('language'), list) and
    'installed_path' in config.keys() and
    isinstance(config.get('installed_path'), str) and
    os.path.isdir(config['installed_path'])
):
    try:
        config = _change_path(config)
    except FileNotFoundError:
        pass


def change_path():
    pywebio.output.put_markdown('[Back](/?app=index) to the index page.')
    tesseract = pywebio.input.input(label='"Tesseract OCR" installed at')
    config_1 = {'installed_path': '', 'language': []}
    try:
        config_1 = _change_path(config_=config_1, user_assigned_path=tesseract)
        if os.path.isdir(tesseract):
            with open('./config.json', 'w') as f:
                json.dump(config_1, f)
            pywebio.output.put_info('Successfully find "Tesseract OCR" here.')
    except FileNotFoundError:
        pywebio.output.put_error('Cannot find "Tesseract OCR" here.')


def index():
    pywebio.output.put_markdown(f"""
        # GUI for "tesseract" OCR
        
        This software is the graphic interface for [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) software.
        When the user inputs a image by uploading a file, the software recognizes the characters in selected language 
        and display the text contained in the image.
        
        ## Tesseract
        
        Installation path of "Tesseract OCR" software:
        ```
        {config['installed_path']}
        ```
        <center><a href="/?app=change_path">Change</a></center>
        
        ## OCR
        
        Please keep patient when waiting for the OCR result. If refreshing the page, you'll loss access to the result.
    """)

    if config['language'] and config['installed_path'] and os.path.isdir(config['installed_path']):
        data = pywebio.input.input_group('', [
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
            pywebio.output.put_markdown("""
            ## Result
            Recognition another image [again](/?app=index).
            """)
            pywebio.output.put_success(content)
    else:
        pywebio.output.put_markdown('Cannot find "Tesseract OCR" or supported language, please assign a installed'
                                    'place by "Change" link above.')


if __name__ == '__main__':
    # Debug
    # pywebio.start_server([index, change_path], auto_open_webbrowser=False, port=5000)
    # Deploy
    pywebio.start_server([index, change_path], auto_open_webbrowser=True)
