import requests
import config
import os
import glob
import zipfile
import imported_modules
import shutil

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
    return rawfile


def unpack_repo_files(rawfile):
    repo_zip_dir = f'{rawfile}_dir'
    repo_zip = zipfile.ZipFile(rawfile)
    repo_zip.extractall(f'{rawfile}_dir')
    return repo_zip_dir


def iterate_repo_files(repo_zip_dir):
    files = glob.glob(repo_zip_dir + '/**/*.py', recursive=True)
    return files


def find_modules(files):
    repo_modules = imported_modules.find_import_modules(files)
    return repo_modules


def check_modules(repo_modules):
    found_modules = []

    if 'requests' in repo_modules:
        found_modules.append('requests')

    if 'beautifulsoup' in repo_modules:
        found_modules.append('BeautifulSoup')

    if 'django' in repo_modules:
        found_modules.append('Django')

    if 'flask' in repo_modules:
        found_modules.append('Flask')

    if 'uuid' in repo_modules:
        found_modules.append('uuid')

    if 'redis' in repo_modules:
        found_modules.append('redis')

    if 'os' in repo_modules:
        found_modules.append('os')

    if 'zipfile' in repo_modules:
        found_modules.append('ZipFile')

    if 'datetime' in repo_modules:
        found_modules.append('datetime')

    if 'modulefinder' in repo_modules:
        found_modules.append('ModuleFinder')

    if 'setuptools' in repo_modules:
        found_modules.append('setuptools')

    if 'collections' in repo_modules:
        found_modules.append('collections')

    if 'openpyxl' in repo_modules:
        found_modules.append('openpyxl')

    if 'bs4' in repo_modules:
        found_modules.append('bs4')

    if 'functools' in repo_modules:
        found_modules.append('functools')

    if 'json' in repo_modules:
        found_modules.append('json')

    if 'glob' in repo_modules:
        found_modules.append('glob')

    return found_modules


def print_result(found_modules):
    print(f'Обнаруженные модули: {found_modules}')


def delete_download_files(rawfile, repo_zip_dir):
    rawfile_dir = rawfile[:-4]
    path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
        rawfile
    )
    rawfile_dir = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
        rawfile_dir
    )
    repo_zip_dir = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
        repo_zip_dir
    )
    os.remove(path)
    shutil.rmtree(rawfile_dir)
    shutil.rmtree(repo_zip_dir)


if __name__ == '__main__':

    repository = get_repository()

    rawfile = get_repo_resource_json(
                repository=repository,
                repo_resource='/zipball/master',
                repo_params=REPO_PARAMS,
            )
    repo_zip_dir = unpack_repo_files(rawfile)
    files = iterate_repo_files(repo_zip_dir)
    repo_modules = imported_modules.find_import_modules(files)
    found_modules = check_modules(repo_modules)
    print_result(found_modules)
    delete_download_files(rawfile, repo_zip_dir)
