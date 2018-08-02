import token_generator
from flask import jsonify


def check_auth_token(token):
    redis_base = token_generator.create_redis_base()
    check_redis_token = redis_base.get(token)
    if check_redis_token is None:
        return jsonify(
            error='You aren\'t authorized, pls email taya.kulagina@gmail.com'
            )
    else:
<<<<<<< HEAD
        return None

=======
        return 'pass'
>>>>>>> b0c8cc1dfd3a0bf0786fa2b2b85bdfc69ad95ec7
