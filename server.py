import scoring_repos
import token_generator
from flask import Flask, request, jsonify
import redis
import uuid


app = Flask(__name__)


@app.route("/evaluate_repo")
def check_token():
    r = token_generator.create_redis_base()
    # redis_token = input('Введите токен \n')
    owner = request.args.get('owner', type=str)
    namerepo = request.args.get('namerepo', type=str)
    token = request.args.get('token', type=str)
    check_redis_token = r.get(token)
    if check_redis_token is None:
        return 'Вы не атворизованы, напишите на почту taya.kulagina@gmail.com'
    else:
        redis_repo = f'{owner}_{namerepo}'
        check_redis_repo = r.get(redis_repo)
        if check_redis_repo is None:
            repository = owner+'/'+namerepo
            check_input = scoring_repos.check_user_input(repository)
            if check_input is None:
                return jsonify(
                    error='Invalid values, please try again')
            else:
                repo_score = scoring_repos.eval_repository(repository)
                insert_redis_result = r.set(redis_repo, repo_score)
                r.expire(insert_redis_result, 2592000)
                return jsonify(rate=str(repo_score))
        else:
            check_redis_repo = check_redis_repo.decode('utf-8')
            return jsonify(rate=str(check_redis_repo))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
