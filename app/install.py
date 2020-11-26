import os
from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile


STATIC_PATH = 'backend/resources'


def move_base_yaml(path):
    my_file = Path(path)
    if my_file.is_file():
        print(f'Copy swagger file to {STATIC_PATH}')
        copyfile(path, f'{STATIC_PATH}/swagger.yaml')
    else:
        raise FileNotFoundError(f"File: {path} doesn't exist")
        

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="swagger.yaml location", dest="filename")
    args = parser.parse_args()

    try:
        move_base_yaml(args.filename)
        os.system('pip install -r backend/packages.txt')
        os.system('builder.py')
    except FileNotFoundError as err:
        print (err.args[0])
