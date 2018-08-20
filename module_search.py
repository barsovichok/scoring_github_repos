import check_modules
import token_generator
import json


def find_api_modules(repository):
    redis_storage = token_generator.create_redis_base()
    rawfile = check_modules.get_repo_resource_json(
        repository=repository,
        repo_resource='/zipball/master',
        repo_params=check_modules.REPO_PARAMS)
    repo_zip_dir = check_modules.unpack_repo_files(rawfile)
    files = check_modules.iterate_repo_py_files(repo_zip_dir)
    repo_modules = check_modules.find_modules(files)
    found_modules = check_modules.check_if_repo_has_seeking_modules(repo_modules)
    redis_repository = '{}{}'.format(repository.replace('/', '_'), '_modules')
    insert_redis_result = redis_storage.set(
        redis_repository, found_modules
    )
    redis_storage.expire(
        insert_redis_result, 2592000
    )
    check_modules.delete_download_files(rawfile, repo_zip_dir)
    return json.dumps(
            {'Found modules': found_modules}
    )
