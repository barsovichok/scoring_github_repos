import token_generator
import check_auth
from flask import Flask, request, jsonify
import redis
import uuid
import check_cache_data



app = Flask(__name__)


@app.route("/evaluate_repo")
def return_auth_result():
    auth_token = check_auth.check_auth_token(request.args.get('token', type=str))
    if auth_token is None:
        check_url = check_cache_data.check_cache_data(
            owner = request.args.get('owner', type=str),
            namerepo = request.args.get('namerepo', type=str),
            redis_base= token_generator.create_redis_base()
    )
        
        return check_url
    else:
        return auth_token
        


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
