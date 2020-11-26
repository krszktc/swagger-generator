import os
import in_place
from shutil import move


STATIC_PATH = 'backend/resources'


def fix_open_api_ruls():
    print('#####-----> Checking open api format rules <-----#####')
    with in_place.InPlace(f'{STATIC_PATH}/openapi.yaml') as yaml:
        for line in yaml:
            if 'format:' in line and 'url' in line:
                line = line.replace('url', 'uri')
            yaml.write(line)


def adjust_swagger():
    print('#####-----> Adjust swagger specification <-----#####')
    with in_place.InPlace(f'{STATIC_PATH}/swagger.yaml') as yaml:
        for line in yaml:
            if 'type: number' in line:
                line = line.replace('number', 'integer')   
            if 'host: some.external.company.com' in line:
                line = line.replace('some.external.company.com', 'localhost:5000')     
            if '- https' in line:
                line = line.replace('- https', '- http')          
            yaml.write(line)            


def generate_models():
    print('#####-----> Generating models <-----#####')
    os.system(
        f'datamodel-codegen --input {STATIC_PATH}/openapi.yaml --output {STATIC_PATH}/generated_models.py')


def generate_ope_api_file():
    print('#####-----> Generating openapi specification <-----#####')
    os.system(
        f'prance convert {STATIC_PATH}/swagger.yaml {STATIC_PATH}/openapi.yaml')


def prepare_client():
    print('#####-----> Installing node modules <-----#####')
    os.chdir('frontend')
    os.system('npm install')
    print('#####-----> Building package <-----#####')
    os.system('npm run build')
    os.chdir('../')


def move_backedn_static():
    print('#####-----> Deploying UI client on Server <-----#####')
    move('frontend/build', f'{STATIC_PATH}/client')


def run_ui_tests():
    print('#####-----> Running Frontend tests <-----#####')
    os.chdir('frontend')
    os.system('npm test')
    os.chdir('../')


def run_backend_tests():
    print('#####-----> Running Backend tests <-----#####')
    os.chdir('backend')
    os.system('pytest')
    os.chdir('../')


if __name__ == '__main__':
    adjust_swagger()
    generate_ope_api_file()
    fix_open_api_ruls()
    generate_models()
    prepare_client()
    move_backedn_static()

    run_ui_tests()
    run_backend_tests()
