import scoring_repos
from flask import Flask, flash, redirect, request, session, abort, jsonify

app = Flask(__name__)


@app.route("/evaluate_repo")
def evaluate_repo():

    owner = request.args.get('owner', type=str)
    namerepo = request.args.get('namerepo', type=str)
    repository = owner+'/'+namerepo

    check_input = scoring_repos.check_user_input(repository)
    if check_input is None:
        return jsonify(
            error='Invalid values, please try again')
    else:
        repo_result = scoring_repos.eval_repository(repository)
        return jsonify(rate=str(repo_result))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
