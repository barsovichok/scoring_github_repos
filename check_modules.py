import requests
import config
import os
import glob
import zipfile
from modulefinder import ModuleFinder


REPO_PARAMS = {
    'client_id': config.CLIENT_ID,
    'client_secret': config.СLIENT_SECRET
}


def get_repository():
    repository = input('Укажите репозиторий в формате owner/repo\n')
    return repository


def get_repo_resource_json(repo_resource, repo_params, repository):
    url = f'https://api.github.com/repos/{repository}{repo_resource}'
    result = requests.get(url, params=repo_params, allow_redirects=True)
    repo_name = f"{repository.replace('/','_')}"
    os.mkdir(f"{repo_name}")
    rawfile = f"{repo_name}.zip"
    with open(rawfile, 'wb') as fd:
        for chunk in result.iter_content(chunk_size=128):
            fd.write(chunk)
    return repo_name


def unpack_repo_files(repo_name):
    repo_zip = zipfile.ZipFile(f'{repo_name}.zip')
    repo_zip.extractall(f'{repo_name}')


def iterate_repo_files(repo_name):
    files = glob.glob(repo_name + '/**/*.py', recursive=True)
    return files


def find_modules(files):
    finder = ModuleFinder()
    for file in files:
        finder.run_script(file)

    for name, mod in finder.modules.items():
        if name == '__main__':
            repo_modules = ','.join(list(mod.globalnames.keys()))
    return repo_modules


def check_modules(repo_modules):
    found_modules = []

    if 'requests' in repo_modules:
        found_modules.append('requests')

    if 'BeautifulSoup' in repo_modules:
        found_modules.append('BeautifulSoup')

    if 'Django' in repo_modules:
        found_modules.append('Django')

    if 'Flask' in repo_modules:
        found_modules.append('Flask')

    return found_modules


def print_result(found_modules):
    print(f'Обнаруженные модули: {found_modules}')


if __name__ == '__main__':

    repository = get_repository()

    repo_name = get_repo_resource_json(
                repository=repository,
                repo_resource='/zipball/master',
                repo_params=REPO_PARAMS,
            )
    unpack_repo_files(repo_name)
    files = iterate_repo_files(repo_name)
    repo_modules = find_modules(files)
    found_modules = check_modules(repo_modules)
    print_result(found_modules)
