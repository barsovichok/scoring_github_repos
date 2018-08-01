import scoring_repos
from flask import Flask, request, jsonify
import redis
import uuid


app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0) 

@app.route("/evaluate_repo")
    

def check_token(): 
    user_email = input('Введите почту разработчика')
    token = str(uuid.uuid4())
    redis_data = r.set(token, user_email)
    print(token, user_email)  
    redis_token = input('Введите токен \n')
    check_redis_token = r.get(redis_token)
    if check_redis_token is None:
        print('Вы не атворизованы, напишите на почту taya.kulagina@gmail.com и получите токен')
    else:
        owner = request.args.get('owner', type=str)
        namerepo = request.args.get('namerepo', type=str)
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
