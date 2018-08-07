import check_modules
from flask import jsonify
import token_generator
import config

 
def find_api_modules(repository):
    redis_storage = token_generator.create_redis_base()
    repo_name = check_modules.get_repo_resource_json(
        repository=repository,
        repo_resource='/zipball/master',
        repo_params={
            'client_id': config.CLIENT_ID,
            'client_secret': config.СLIENT_SECRET
        },
    )
    check_modules.unpack_repo_files(repo_name)
    files = check_modules.iterate_repo_files(repo_name)
    repo_modules = check_modules.find_modules(files)
    found_modules = check_modules.check_modules(repo_modules)
    insert_redis_result = redis_storage.set(
        f'{repository}_modules', found_modules
    )
    redis_storage.expire(
        insert_redis_result, 2592000
    )
    return json.dumps(
            {'Found modules': found_modules}
    )