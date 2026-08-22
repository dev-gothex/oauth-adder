import json
from pathlib import Path



class Config():
    def __init__(self,path):
        self.path=path
        self.data=self.load()
    def load(self):
        with open(self.path,'r') as f:
            return json.load(f)
    def get(self,key):
        return self.data.get(key)
class values:
    BASE_DIR = Path(__file__).resolve().parent.parent
    def __init__(self):
        self.config = self.BASE_DIR / "config.json"
    def ua(self):
        return Config(self.config).get("useragent")

    def client_id(self):
        return Config(self.config).get("client_id")

    def auth_url(self):
        client_id = Config(self.config).get("client_id")
        redirect_url = Config(self.config).get("redirect_url")
        response_type = Config(self.config).get("response_type")
        scope = Config(self.config).get("scope")

        return f'https://discord.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_url}&response_type={response_type}&scope={scope}'

    def token(self):
        with open('token.txt', 'r') as f:
            return f.readline().strip()

