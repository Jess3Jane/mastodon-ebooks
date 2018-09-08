import markovify
import json
import time
from mastodon import Mastodon

api_base_url = "https://botsin.space" #todo: this shouldn't be hardcoded

client = Mastodon(
        client_id="clientcred.secret", 
        access_token="usercred.secret", 
        api_base_url=api_base_url)

with open("corpus.txt", encoding="utf-8") as fp:
  model = markovify.NewlineText(fp.read())

print("tooting")
sentence = None
# you will make that damn sentence
while sentence is None:
	sentence = model.make_sentence(tries=100000)
toot = sentence.replace("\0", "\n")
client.toot(toot)
print("Created toot: {}".format(toot))
