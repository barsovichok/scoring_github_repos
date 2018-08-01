import server
import scoring_repos
import token_generator
from flask import Flask, request, jsonify
import redis
import uuid


def return_r(r):
    return r

def make_redis_repo(owner, namerepo):
    redis_repo = f'{owner}_{namerepo}'
    return redis_repo

def get_redis_repo(redis_repo, r):
    get_redis_repo = r.get(redis_repo)
    return get_redis_repo

def check_redis_repo(get_redis_repo, owner, namerepo):
    if get_redis_repo is None:
        repository = owner+'/'+namerepo
        check_input = scoring_repos.check_user_input(repository)
        if check_input is None:
            return jsonify(
                error='Invalid values, please try again')
        else:
            repo_score = scoring_repos.eval_repository(repository)
            insert_redis_result = r.set(redis_repo, repo_score)
            r.expire(insert_redis_result, 2592000)
            return jsonify(rate=str(repo_score))
    else:
        check_redis_repo = check_redis_repo.decode('utf-8')
        return jsonify(rate=str(check_redis_repo))

def result(result):
    return result

r = server.return_r()
owner = server.return_owner()
namerepo = server.return_namerepo()
redis_repo = make_redis_repo()
get_redis_repo = get_redis_repo(redis_repo, r)
result = check_redis_repo(get_redis_repo, owner, namerepo)