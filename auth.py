from flask import Response, jsonify
import json
import token_generator


def check_auth_token(token):
    redis_base = token_generator.create_redis_base()
    redis_token = redis_base.get(token)
    if redis_token is None:
        return Response('{error: You aren\'t authorized}', status=401, mimetype='application/json')
    else:
        return None
