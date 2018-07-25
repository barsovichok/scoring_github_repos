import scoring_repos
from flask import Flask, flash, redirect, request, session, abort, jsonify

app = Flask(__name__)


@app.route("/evaluate_repo")
def evaluate_repo():

    owner = request.args.get('owner', type=str)
    namerepo = request.args.get('namerepo', type=str)
    date_offset = 10
    date_delta = 30
    user = owner+'/'+namerepo
    check_input = scoring_repos.check_user_input(user)
    if check_input == None:
        return jsonify(
            error='Invalid values, please try again')
    else:
        repo_params = scoring_repos.return_repo_params()
        repo_pull_params = scoring_repos.return_repo_pull_params()
        repo_contributors_json = scoring_repos.get_repo_resource_json(
            user=user,
            repo_resource='/contributors',
            repo_params=repo_params,
        )

        repo_readme_json = scoring_repos.get_repo_resource_json(
            user=user,
            repo_resource='/readme',
            repo_params=repo_params,
        )

        repo_pull_requests_json = scoring_repos.get_repo_resource_json(
            user=user,
            repo_resource='/pulls',
            repo_params=repo_pull_params,
        )

        repo_files_json = scoring_repos.get_repo_resource_json(
            user=user,
            repo_resource='/contents',
            repo_params=repo_params,
        )

        repo_json = scoring_repos.get_repo_json(
            user=user,
            repo_params=repo_params,
        )

        repo_contributors = scoring_repos.get_repo_contributors(
            repo_contributors_json
        )

        pull_requests = scoring_repos.get_repo_pull_requests(
            repo_pull_requests_json,
            date_offset,
        )

        pull_request_amount = scoring_repos.get_pull_requests_date_delta(
            pull_requests,
            date_delta
        )

        repo_files = scoring_repos.get_repo_file(repo_files_json)
        repo_result = scoring_repos.count_repo_result(
            repo_files,
            repo_contributors,
            pull_requests,
            repo_readme_json,
            repo_json,
            pull_request_amount
        )

        rate = 'rate'

        return jsonify(
            rate=repo_result,
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
