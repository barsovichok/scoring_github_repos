from flask import Response
import json
import config
import redis
import token_generator


def check_auth_token(token):
    redis_base = token_generator.create_redis_base()
    check_redis_token = redis_base.get(token)
    if check_redis_token is None:
        auth_error = json.dumps(
            {'error': 'You aren\'t authorized'}
        )
        return Response(auth_error, status=401, mimetype='application/json')
    else:
        return None
