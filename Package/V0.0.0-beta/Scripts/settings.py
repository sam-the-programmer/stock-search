import json
import os


def get_new() -> bool:
    if not os.path.isdir(r'C:\ProgramData\Stock Search'):
        return True
    else:
        os.makedirs(os.path.dirname('C:\ProgramData\Stock Search'))
        return False

def get_welcome_screen() -> bool:
    with open(r'C:\ProgramData\Stock Search\app_data.json') as file:
        saved_data = json.load(file)
    return bool(saved_data['welcome_screen'])

def set_welcome_screen(value: bool):
    with open(r'C:\ProgramData\Stock Search\app_data.json') as file:
        saved_data = json.load(file)
        
    with open(r'C:\ProgramData\Stock Search\app_data.json', 'w') as file:
        saved_data['welcome_screen'] = value
        file.write(json.dumps(saved_data))