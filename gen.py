import markovify
import json
from mastodon import Mastodon

with open("settings.json") as fp:
    settings = json.load(fp)

api_base_url = settings.setdefault("api_base_url", "https://botsin.space")

client = Mastodon(
        client_id="clientcred.secret", 
        access_token="usercred.secret", 
        api_base_url=api_base_url)

with open("corpus.txt") as fp:
    model = markovify.NewlineText(fp.read())

print("Running...")
while True:
    print("tooting")
    client.toot(model.make_sentence().replace(chr(31), "\n"))
    print("sleeping")
    time.sleep(60*60*3)
