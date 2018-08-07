import auth
from flask import Flask, request
import cache_data
import config
import token_generator
import check_modules
import json


app = Flask(__name__)


@app.route("/evaluate_repo")
def return_auth_result():
    auth_token = auth.check_auth_token(
        request.args.get('token', type=str)
    )
    if auth_token is None:
        check_url = cache_data.check_cache_data(
            owner=request.args.get('owner', type=str),
            namerepo=request.args.get('namerepo', type=str),
            redis_base=token_generator.create_redis_base()
        )
        return check_url
    else:
        return auth_token


@app.route("/check_repo_modules")
def return_check_modules():
    auth_token = auth.check_auth_token(
        request.args.get('token', type=str)
    )
    if auth_token is None:
        owner = request.args.get('owner', type=str)
        namerepo = request.args.get('namerepo', type=str)
        repository = f'{owner}/{namerepo}'
        REPO_PARAMS = {
            'client_id': config.CLIENT_ID,
            'client_secret': config.СLIENT_SECRET
        }
        repo_name = check_modules.get_repo_resource_json(
                repository=repository,
                repo_resource='/zipball/master',
                repo_params=REPO_PARAMS,
            )
        check_modules.unpack_repo_files(repo_name)
        files = check_modules.iterate_repo_files(repo_name)
        repo_modules = check_modules.find_modules(files)
        found_modules = check_modules.check_modules(repo_modules)
        return json.dumps(
            {'Found modules': found_modules}
        )
    else:
        return auth_token


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
