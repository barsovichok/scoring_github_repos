import module_search
import json


def check_cache_data(owner, namerepo, redis_base):
    repository_url = f'{owner}/{namerepo}'
    redis_repository = f'{owner}_{namerepo}_modules'
    check_redis_repo = redis_base.get(redis_repository)
    if check_redis_repo is None:
        repo_modules = module_search.find_api_modules(
            repository=repository_url
        )
        return repo_modules
    else:
        check_redis_repo = check_redis_repo.decode('utf-8')
        return json.dumps(
            {'Found modules': check_redis_repo}
        )
