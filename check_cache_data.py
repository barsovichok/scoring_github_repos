import scoring_repos
from flask import jsonify


def check_cache_data(owner, namerepo, redis_base):
    redis_repo = f'{owner}_{namerepo}'
    check_redis_repo = redis_base.get(redis_repo)
    if check_redis_repo is None:
        repository = owner+'/'+namerepo
        check_input = scoring_repos.check_user_input(repository)
        if check_input is None:
            return jsonify(
                error='Invalid values, please try again')
        else:
            repo_score = scoring_repos.eval_repository(repository)
            insert_redis_result = redis_base.set(redis_repo, repo_score)
            redis_base.expire(insert_redis_result, 2592000)
            return jsonify(rate=repo_score)
    else:
        check_redis_repo = check_redis_repo.decode('utf-8')
<<<<<<< HEAD:check_cache_data.py
        return jsonify(rate=check_redis_repo)
=======
        return jsonify(rate=str(check_redis_repo))
>>>>>>> b0c8cc1dfd3a0bf0786fa2b2b85bdfc69ad95ec7:check_cash_data.py
