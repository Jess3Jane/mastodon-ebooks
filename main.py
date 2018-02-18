from mastodon import Mastodon
from getpass import getpass
from os import path
import json
import re

api_base_url = "https://botsin.space"

if not path.exists("clientcred.secret"):
    print("No clientcred.secret, registering application")
    Mastodon.create_app("ebooks", api_base_url=api_base_url, to_file="clientcred.secret")

if not path.exists("usercred.secret"):
    print("No usercred.secret, registering application")
    email = input("Email: ")
    password = getpass("Password: ")
    client = Mastodon(client_id="clientcred.secret", api_base_url=api_base_url)
    client.log_in(email, password, to_file="usercred.secret")

def remove_tags(text):
    text = text.strip().replace("<br>", chr(31))
    TAG_RE = re.compile(r'<[^>]+>')
    next_re = TAG_RE.sub('', text)
    last = re.sub(r"(?:\@|https?\"//)\S+", "", next_re)
    if len(last) > 0:
        if last[0] == " ":
            last = last[1:]
    else:
        last = ""
    return last 

def get_toots(client, id):
    i = 0
    toots = client.account_statuses(id)
    while toots is not None:
        for toot in toots:
            if toot.spoiler_text == "" and toot.reblog is None and toot.visibility in ["public", "unlisted"]:
                yield remove_tags(toot.content)
        toots = client.fetch_next(toots)
        i += 1
        if i%10 == 0:
            print(i)

client = Mastodon(
        client_id="clientcred.secret", 
        access_token="usercred.secret", 
        api_base_url=api_base_url)

me = client.account_verify_credentials()
following = client.account_following(me.id)

with open("corpus.txt", "w+") as fp:
    for f in following:
        print(f.username)
        for t in get_toots(client, f.id):
            fp.write(t + "\n")
