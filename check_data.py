import repo_scoring
import token_generator


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
