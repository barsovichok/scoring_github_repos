import scoring_repos
from flask import Flask, request, jsonify
import redis


app = Flask(__name__)


@app.route("/evaluate_repo")
def evaluate_repo():

    owner = request.args.get('owner', type=str)
    namerepo = request.args.get('namerepo', type=str)
    redis_repo = owner+'_'+namerepo
    r = redis.Redis(host='localhost', port=6379, db=0)
    check_redis_repo = r.get(redis_repo)
    if check_redis_repo is None:
        repository = owner+'/'+namerepo
        check_input = scoring_repos.check_user_input(repository)
        if check_input is None:
            return jsonify(
                error='Invalid values, please try again')
        else:
            repo_result = scoring_repos.eval_repository(repository)
            insert_redis_result = r.set(redis_repo,repo_result)
            return jsonify(rate=str(repo_result))
    else:
        check_redis_repo = check_redis_repo.decode('utf-8')
        return jsonify(rate=str(check_redis_repo))


    
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
