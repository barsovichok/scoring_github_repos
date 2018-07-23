import scoring_repos
from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Flask App!"
 
#@app.route("/hello/<string:name>")
@app.route("/evaluate_repo/<string:owner>/<string:namerepo>")
def hello(owner, namerepo):

    user = str(owner+'/'+namerepo)

    print_i = scoring_repos.print_repo_result(987954)

 
    return render_template(
        'test.html',**locals())
 
if __name__ == "__main__":
    namerepo = input('fiasko_bro')
    owner = input('devmanorg')
    app.run(host='0.0.0.0', port=80)
    #get_score()

