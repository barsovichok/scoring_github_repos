import repo_scoring
import token_generator
import module_scoring


def check_auth_token(token):
    redis_base = token_generator.create_redis_base()
    redis_token = redis_base.get(token)
    if redis_token is None:
        return False
    else:
        return True


def check_cache_data(owner, namerepo):
    redis_repo = f'{owner}_{namerepo}'
    redis_storage = token_generator.create_redis_base()
    redis_repo = redis_storage.lindex(redis_repo, 0)
    if redis_repo is None:
        return False
    else:
        return True


def check_user_input(owner, namerepo):
    repository = f'{owner}/{namerepo}'
    check_input = repo_scoring.check_user_input(repository)
    if check_input is None:
        return False
    else:
        return True


def get_redis_data(owner, namerepo):
    redis_base = token_generator.create_redis_base()
    redis_repo = f'{owner}_{namerepo}'
    repo_scope = redis_base.lindex(redis_repo, 0)
    language = redis_base.lindex(redis_repo, 1)
    repo_scope = repo_scope.decode('utf-8')
    language = language.decode('utf-8')
    return repo_scope, language


def evaluate_repo(owner, namerepo):
    repository = f'{owner}/{namerepo}'
    repo_score = repo_scoring.eval_repository(repository)
    return repo_score


def find_repo_languages(owner, namerepo):
    repository = f'{owner}/{namerepo}'
    languages = repo_scoring.repository_language(repository)
    return languages


def insert_redis_data(owner, namerepo, languages, repo_score):
    redis_storage = token_generator.create_redis_base()
    redis_repository = f'{owner}_{namerepo}'
    insert_repo_result = redis_storage.rpush(
            redis_repository,
            repo_score
        )
    insert_language_result = redis_storage.rpush(
            redis_repository,
            languages
        )
    redis_storage.expire(
            insert_repo_result, 2592000
        )


def check_module_cache(owner, namerepo):
    redis_base = token_generator.create_redis_base()
    redis_repository = f'{owner}_{namerepo}_modules'
    check_redis_repo = redis_base.get(redis_repository)
    if check_redis_repo is None:
        return False
    else:
        return True


def get_redis_module_data(owner, namerepo):
    redis_base = token_generator.create_redis_base()
    redis_repository = f'{owner}_{namerepo}_modules'
    check_redis_repo = redis_base.get(redis_repository)
    check_redis_repo = check_redis_repo.decode('utf-8')
    return check_redis_repo


def find_api_modules(owner, namerepo):
    repository=f'{owner}/{namerepo}'
    redis_storage = token_generator.create_redis_base()
    rawfile = module_scoring.get_repo_resource_json(
        repository=repository,
        repo_resource='/zipball/master',
        repo_params=module_scoring.REPO_PARAMS)
    repo_zip_dir =module_scoring.unpack_repo_files(rawfile)
    files = module_scoring.iterate_repo_py_files(repo_zip_dir)
    repo_modules = module_scoring.find_import_modules(files)
    found_modules = module_scoring.check_if_repo_has_seeking_modules(repo_modules)
    redis_repository = '{}{}'.format(repository.replace('/', '_'), '_modules')
    insert_redis_result = redis_storage.set(
        redis_repository, found_modules
    )
    redis_storage.expire(
        insert_redis_result, 2592000
    )
    module_scoring.delete_download_files(rawfile, repo_zip_dir)
    return found_modules

