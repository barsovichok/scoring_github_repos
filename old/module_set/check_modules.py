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


def iterate_repo_py_files(repo_zip_dir):
    files = glob.glob(repo_zip_dir + '/**/*.py', recursive=True)
    return files


def find_modules(files):
    repo_modules = imported_modules.find_import_modules(files)
    return repo_modules


def check_if_repo_has_seeking_modules(repo_modules):
    found_modules = []
    for module in repo_modules:
        if module in config.MODULES:
            found_modules.append(module)

    clear_modules = set(found_modules)
    found_modules = list(clear_modules)
    return found_modules


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

    repository = input('Укажите репозиторий в формате owner/repo\n')

    rawfile = get_repo_resource_json(
                repository=repository,
                repo_resource='/zipball/master',
                repo_params=REPO_PARAMS,
            )
    repo_zip_dir = unpack_repo_files(rawfile)
    files = iterate_repo_files(repo_zip_dir)
    repo_modules = imported_modules.find_import_modules(files)
    found_modules = check_if_repo_has_seeking_modules(repo_modules)
    print(f'Обнаруженные модули: {found_modules}')
    delete_download_files(rawfile, repo_zip_dir)
