import token_generator
import check_auth
import check_cash_data
from flask import Flask, request


app = Flask(__name__)


@app.route("/evaluate_repo")
def return_auth_result():
    auth_token = check_auth.check_auth_token(
        request.args.get('token', type=str)
    )
    if auth_token != 'pass':
        return auth_token
    else:
        check_url = check_cash_data.check_cash_data(
            owner=request.args.get('owner', type=str),
            namerepo=request.args.get('namerepo', type=str),
            r=token_generator.create_redis_base()
        )
        return check_url


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
