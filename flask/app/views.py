from app import app
import requests
from flask import render_template_string, redirect, request, jsonify, url_for
import json

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/line-login/')
def login():
    url = "https://notify-bot.line.me/oauth/authorize"
    url = url + "?response_type=code"
    url = url + "&client_id=2FiajbKaqThu1rRS8CdJYM"
    url = url + "&redirect_uri=https://notify.npworld.info/callback/"
    url = url + "&scope=notify"
    url = url + "&state=mujxi7dKk"
    # req = requests.get('https://notify-bot.line.me/oauth/authorize', params = {
    #     "response_type": "code",
    #     "client_id": "2FiajbKaqThu1rRS8CdJYM",
    #     "redirect_uri": "https://notify.npworld.info/callback/",
    #     "scope": "notify",
    #     "state": "mujxi7dKk"
    # })
    return redirect(url)

@app.route('/callback/')
def callback():
    code = request.args.get('code')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post('https://notify-bot.line.me/oauth/token', data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://notify.npworld.info/callback/",
        "client_id": "2FiajbKaqThu1rRS8CdJYM",
        "client_secret": "vTDF9Wi1tWzhM79PQpSp7pqDUhoK6Bx5jF8vGDOD9l0"
    }, headers=headers).json()
    access_token = res.get("access_token")
    # เก็บ access_token ลง db
    return access_token
    # return redirect(url_for('complete'))

@app.route('/line_connection_complete/')
def complete():
   return "Complete"
    
@app.route('/post_message/', methods=["POST"])
def post_message():
    _data = request.json
    message = _data['message']
    id = _data['uid']
    # get access_token from db by uid
    access_token = 'oYW2nJlmUyyucuI3uSNci9OWyerUa2e9Cf30b4Qn16Y'
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Bearer " + access_token}
    res = requests.post('https://notify-api.line.me/api/notify', data={
        "message": message
    }, headers=headers).json()
    return jsonify(res)
