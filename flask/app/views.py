from app import app
import requests
from flask import render_template_string, redirect

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
    code = requests.args.get('code')
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    req = requests.post('https://notify-bot.line.me/oauth/token', data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://notify.npworld.info/callback/",
        "client_id": "2FiajbKaqThu1rRS8CdJYM",
        "client_secret": "vTDF9Wi1tWzhM79PQpSp7pqDUhoK6Bx5jF8vGDOD9l0"
    }, headers=headers)
    return req + ' and ' + req.text
    

