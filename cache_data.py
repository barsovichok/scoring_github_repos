import evaluation_repo
from flask import jsonify


def check_cache_data(owner, namerepo, redis_base):
    redis_repo = f'{owner}_{namerepo}'
    check_redis_repo = redis_base.get(redis_repo)
    if check_redis_repo is None:
        repo_scope = evaluation_repo.eval_repo(owner, namerepo)
        return repo_scope
    else:
        check_redis_repo = check_redis_repo.decode('utf-8')
        return jsonify(
            rate=check_redis_repo,
            language=check_redis_repo
        )
