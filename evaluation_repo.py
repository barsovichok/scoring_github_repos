import repo_scoring
from flask import jsonify
import token_generator


def eval_repo(owner, namerepo):
    repository = f'{owner}/{namerepo}'
    redis_storage = token_generator.create_redis_base()
    check_input = repo_scoring.check_user_input(repository)
    if check_input is None:
        return jsonify(
                error='Invalid values, please try again')
    else:
        repo_score = repo_scoring.eval_repository(repository)
        insert_redis_result = redis_storage.set(repository, repo_score)
        redis_storage.expire(insert_redis_result, 2592000)
        return jsonify(
                rate=repo_score
        )