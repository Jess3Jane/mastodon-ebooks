from mastodon import Mastodon
from getpass import getpass
from os import path
from bs4 import BeautifulSoup
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

def parse_toot(toot):
	if toot.spoiler_text != "": return
	if toot.reblog is not None: return
	if toot.visibility not in ["public", "unlisted"]: return

	soup = BeautifulSoup(toot.content, "html.parser")
	
	# pull the mentions out
	# for mention in soup.select("span.h-card"):
	#     mention.unwrap()

	# for mention in soup.select("a.u-url.mention"):
	#     mention.unwrap()

	# we will destroy the mentions until we're ready to use them
	# someday turbocat, you will talk to your sibilings
	for mention in soup.select("span.h-card"):
		mention.decompose()
	
	# make all linebreaks actual linebreaks
	for lb in soup.select("br"):
		lb.insert_after("\n")
		lb.decompose()

	# make each p element its own line because sometimes they decide not to be
	for p in soup.select("p"):
		p.insert_after("\n")
		p.unwrap()
	
	# keep hashtags in the toots
	for ht in soup.select("a.hashtag"):
		ht.unwrap()

	# unwrap all links (i like the bots posting links)
	for link in soup.select("a"):
		link.insert_after(link["href"])
		link.decompose()

	text = map(lambda a: a.strip(), soup.get_text().strip().split("\n"))

	# next up: store this and patch markovify to take it
	# return {"text": text, "mentions": mentions, "links": links}
	# it's 4am though so we're not doing that now, but i still want the parser updates
	return "\0".join(list(text))

def get_toots(client, id):
	i = 0
	toots = client.account_statuses(id)
	while toots is not None:
		for toot in toots:
			t = parse_toot(toot)
			if t != None:
				yield t
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

with open("corpus.txt", "w+", encoding="utf-8") as fp:
	for f in following:
		print("Downloading toots for user @{}".format(f.username))
		for t in get_toots(client, f.id):
			fp.write(t + "\n")
