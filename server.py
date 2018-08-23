from flask import Flask, request, jsonify, Response, render_template, redirect
import config
import check_data


app = Flask(__name__)


@app.route("/evaluate_repo")
def return_evaluate_repo():
    auth_result = check_data.check_auth_token(
        request.args.get('token', type=str)
    )
    if auth_result is True:
        redis_repo = check_data.check_cache_data(
            owner=request.args.get('owner', type=str),
            namerepo=request.args.get('namerepo', type=str)
        )
        if redis_repo is False:
            repo = check_data.check_user_input(
                owner=request.args.get('owner', type=str),
                namerepo=request.args.get('namerepo', type=str)
            )
            if repo is False:
                return jsonify(error=config.INVALID_ERROR)
            else:
                repo_score = check_data.evaluate_repo(
                    owner=request.args.get('owner', type=str),
                    namerepo=request.args.get('namerepo', type=str)
                )
                languages = check_data.find_repo_languages(
                    owner=request.args.get('owner', type=str),
                    namerepo=request.args.get('namerepo', type=str)
                )
                insert_data = check_data.insert_redis_data(
                    owner=request.args.get('owner', type=str),
                    namerepo=request.args.get('namerepo', type=str),
                    repo_score=repo_score,
                    languages=languages,
                )
                return jsonify(repo_score=repo_score, language=languages)
        else:
            repo_score, language = check_data.get_redis_data(
                owner=request.args.get('owner', type=str),
                namerepo=request.args.get('namerepo', type=str)
            )
            return jsonify(repo_score=repo_score, language=language)
    else:
        return Response(
            config.AUTHORIZE_ERROR,
            status=401,
            mimetype='application/json'
        )


@app.route("/check_repo_modules")
def return_module_auth_result():
    auth_result = check_data.check_auth_token(
        request.args.get('token', type=str)
    )
    if auth_result is True:
        check_url = check_data.check_module_cache(
            owner=request.args.get('owner', type=str),
            namerepo=request.args.get('namerepo', type=str)
        )
        if check_url is False:
            repo = check_data.check_user_input(
                owner=request.args.get('owner', type=str),
                namerepo=request.args.get('namerepo', type=str)
            )
            if repo is False:
                return jsonify(error=config.INVALID_ERROR)
            else:
                repo_modules = check_data.find_api_modules(
                    owner=request.args.get('owner', type=str),
                    namerepo=request.args.get('namerepo', type=str)
                )
            return jsonify(found_modules=repo_modules)
        else:
            found_modules = check_data.get_redis_module_data(
                owner=request.args.get('owner', type=str),
                namerepo=request.args.get('namerepo', type=str)
            )
            return jsonify(found_modules=found_modules)
    else:
        return Response(
            config.AUTHORIZE_ERROR,
            status=401,
            mimetype='application/json'
        )


@app.route('/')
def start():
    return render_template('render_template.html')


@app.route('/', methods=['POST'])
def my_form_post():
    namerepo = request.form['repo']
    owner = request.form['owner']
    token = request.form['token']
    choose_repo_evaluate = request.form['choose_repo_evaluate']
    if choose_repo_evaluate == 'Оценить репозиторий':
        return redirect(
            f'/evaluate_repo?namerepo={namerepo}&owner={owner}&token={token}'
        )
    else:
        return redirect(
            f'/check_repo_modules?namerepo={namerepo}&owner={owner}&token={token}'
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

