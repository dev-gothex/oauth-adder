from flask import Flask, redirect, request
import os
from dotenv import load_dotenv
import requests
app = Flask(__name__)
load_dotenv()


#take these from env/config or hardcode them 
CLIENT_ID = os.environ["DISCORD_CLIENT_ID"]
CLIENT_SECRET = os.environ["DISCORD_CLIENT_SECRET"]
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
REDIRECT_URI = os.environ["DISCORD_REDIRECT_URI"]
api = "https://discord.com/api" #hardcode it or take it from config.json/.env

@app.route("/authorize")
def authorize():
    url = (
        f"{api}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify%20guilds.join"
    )
    return redirect(url)


@app.route('/callback')
def callback():
    code = request.args.get("code")
    if not code:
        return "missing code", 400
    headers= {"Content-Type": "application/x-www-form-urlencoded"}
    response=requests.post(
        f"{api}/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers=headers)
    response.raise_for_status()
    data = response.json()
    access_token = data["access_token"]
    refresh_token=data.get("refresh_token")
    user_response = requests.get(
        f"{api}/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_response.raise_for_status()
    user_id = user_response.json()["id"]
    with open("i.txt", "a") as f:
        f.write(f"{user_id}:{access_token}:{refresh_token}\n")
    return f"Successfully added auth, user_id = {user_id}"

if __name__ == "__main__":
    app.run(port=5000, debug=False)
