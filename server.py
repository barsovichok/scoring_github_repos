import auth
from flask import Flask, request, jsonify, Response
import cache_data
import token_generator
import modules_cache
import config
import json


app = Flask(__name__)


@app.route("/evaluate_repo")
def return_auth_result():
    auth_result = auth.check_auth_token(
        request.args.get('token', type=str)
    )
    if auth_result is None:
        repo_result = cache_data.check_cache_data(
            owner=request.args.get('owner', type=str),
            namerepo=request.args.get('namerepo', type=str),
            redis_base=token_generator.create_redis_base()
        )
        if repo_result == config.INVALID_ERROR:
            return jsonify(error=repo_result)
        else:
            repo_score, language = repo_result
            return jsonify(repo_score=repo_score, language=language)
    else:
        return Response(json.dumps({'error':auth_result}), status=401, mimetype='application/json')


@app.route("/check_repo_modules")
def return_check_modules():
    auth_token = auth.check_auth_token(
        request.args.get('token', type=str)
    )
    if auth_token is None:

        check_url = modules_cache.check_cache_data(
            owner=request.args.get('owner', type=str),
            namerepo=request.args.get('namerepo', type=str),
            redis_base=token_generator.create_redis_base()
        )
        return jsonify(check_url)
    else:
        return jsonify(auth_token)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
