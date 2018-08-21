from flask import Response, jsonify
import json
import token_generator
import config


def check_auth_token(token):
    redis_base = token_generator.create_redis_base()
    redis_token = redis_base.get(token)
    if redis_token is None:
        return False
    else:
        return True
