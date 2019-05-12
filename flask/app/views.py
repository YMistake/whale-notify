from app import app
import requests
from flask import render_template_string, redirect, request, jsonify, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class LineToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, unique=True)
    access_token = db.Column(db.String(1000), nullable=False)

    def __init__(self, uid, access_token):
        self.uid = uid
        self.access_token = access_token

class LineTokenSchema(ma.Schema):
    class Meta:
        fields = ('id', 'uid', 'access_token')

line_token_schema = LineTokenSchema(strict=True)
line_tokens_schema = LineTokenSchema(many=True, strict=True)

@app.route('/')
def index():
    return "Whale Notify"

# use for connect to line notify
@app.route('/line-login/', methods=["GET"])
def login():
    uid = request.args.get('uid')
    query = LineToken.query.get(uid)
    url = "https://notify-bot.line.me/oauth/authorize"
    url = url + "?response_type=code"
    url = url + "&client_id=2FiajbKaqThu1rRS8CdJYM"
    url = url + "&redirect_uri=https://notify.npworld.info/callback/" + uid + "/"
    url = url + "&scope=notify"
    url = url + "&state=mujxi7dKk"
    url = url + "&response_mode=form_post"
    # check token for this uid
    if query:
        # have token then delete and return login page
        LineToken.query.filter_by(uid=uid).delete()
        db.session.commit()
        return redirect(url)
    else:
        # dont have token then return login page
        return redirect(url)

@app.route('/revoke_token/', methods=["GET"])
def revoke():
    uid = request.args.get('uid')
    query = LineToken.query.get(uid)
    if query:
        result = line_token_schema.dump(query)
        access_token = result.data['access_token']
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Bearer " + access_token}
        res = requests.post('https://notify-api.line.me/api/revoke', headers=headers).json()
        if res['status'] == 200:
            LineToken.query.filter_by(uid=uid).delete()
            db.session.commit()
            return jsonify(res)
        else:
            return jsonify(res)
    else:
        return jsonify({"status": "successfull", "is_login": 0})

    
# callback function from line when loged in
# They will send 'code' and 'state' back to us
# use 'code' for get access token from line
@app.route('/callback/<int:uid>/', methods=["POST"])
def callback(uid):
    code = request.args.get('code')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post('https://notify-bot.line.me/oauth/token', data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://notify.npworld.info/callback/" + uid + "/",
        "client_id": "2FiajbKaqThu1rRS8CdJYM",
        "client_secret": "vTDF9Wi1tWzhM79PQpSp7pqDUhoK6Bx5jF8vGDOD9l0"
    }, headers=headers).json()
    access_token = res.get("access_token")
    # store access token and uid in db to use in another API
    keep_token = LineToken(uid, access_token)
    db.session.add(keep_token)
    db.session.commit()
    return redirect(url_for('complete'))

# @app.route('/test_db/<int:uid>', methods=["GET"])
# def test(uid):
#     access_token = LineToken.query.get(uid)
#     result = line_token_schema.dump(access_token)
#     return jsonify(result.data['access_token'])

@app.route('/line_connection_complete/')
def complete():
   return render_template('complete.html')
    
@app.route('/post_message/', methods=["POST"])
def post_message():
    _data = request.json
    message = _data['message']
    uid = _data['uid']
    # get access_token from db by uid
    # access_token = 'oYW2nJlmUyyucuI3uSNci9OWyerUa2e9Cf30b4Qn16Y'
    query = LineToken.query.get(uid)
    result = line_token_schema.dump(query)
    access_token = result.data['access_token']
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Bearer " + access_token}
    res = requests.post('https://notify-api.line.me/api/notify', data={
        "message": message
    }, headers=headers).json()
    return jsonify(res)

@app.route('/check_status', methods=["GET"])
def check_status():
    uid = request.args.get('uid')
    query = LineToken.query.get(uid)
    if query:
        result = line_token_schema.dump(query)
        access_token = result.data['access_token']
        headers = {"Authorization": "Bearer " + access_token}
        res = requests.get('https://notify-api.line.me/api/status', headers=headers).json()
        return jsonify(res)
    else:
        return jsonify({"status": "successfull", "is_login": 0})