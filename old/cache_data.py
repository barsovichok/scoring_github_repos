import evaluation_repo
from flask import jsonify


def check_cache_data(owner, namerepo, redis_base):
    redis_repo = f'{owner}_{namerepo}'
    repo_scope = redis_base.lindex(redis_repo, 0)
    language = redis_base.lindex(redis_repo, 1)
    if repo_scope is None:
        repo_scope = evaluation_repo.evaluate_repo(owner, namerepo)
        return repo_scope
    else:
        repo_scope = repo_scope.decode('utf-8')
        language = language.decode('utf-8')
        return repo_scope, language