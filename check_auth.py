import token_generator
from flask import jsonify, Response


def check_auth_token(token):
    redis_base = token_generator.create_redis_base()
    check_redis_token = redis_base.get(token)
    if check_redis_token is None:
        return  Response("{'error':'You aren\'t authorized, pls email taya.kulagina@gmail.com'}", status=401, mimetype='application/json')
    else:
        return None
