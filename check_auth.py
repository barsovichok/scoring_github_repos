import scoring_repos
import token_generator
from flask import Flask, request, jsonify
import redis
import uuid


def check_auth_token(token):
    redis_base = token_generator.create_redis_base()
    check_redis_token = redis_base.get(token)
    if check_redis_token is None:
        return jsonify(
            error='You aren\'t authorized, pls email taya.kulagina@gmail.com'
            )
    else:
        return None

