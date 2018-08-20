import repo_scoring
from flask import jsonify
import token_generator
import config


def evaluate_repo(owner, namerepo):
    repository = f'{owner}/{namerepo}'
    redis_storage = token_generator.create_redis_base()
    check_input = repo_scoring.check_user_input(repository)
    if check_input is None:
        return config.INVALID_ERROR
    else:
        repo_score = repo_scoring.eval_repository(repository)
        language = repo_scoring.repository_language(repository)
        redis_repository = f'{owner}_{namerepo}'
        insert_redis_result = redis_storage.rpush(
            redis_repository,
            repo_score 
        )
        insert_redis = redis_storage.rpush(
            redis_repository,
            language
        )
        redis_storage.expire(
            insert_redis_result, 2592000
        )
        return repo_score, language
