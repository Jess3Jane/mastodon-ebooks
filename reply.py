#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import mastodon
import os, random, re
import create
from bs4 import BeautifulSoup

api_base_url = "https://botsin.space"
client = mastodon.Mastodon(
        client_id="clientcred.secret", 
        access_token="usercred.secret", 
        api_base_url=api_base_url)

def extract_toot(toot):
	#copied from main.py, see there for comments
	soup = BeautifulSoup(toot, "html.parser")
	for lb in soup.select("br"):
		lb.insert_after("\n")
		lb.decompose()
	for p in soup.select("p"):
		p.insert_after("\n")
		p.unwrap()
	for ht in soup.select("a.hashtag"):
		ht.unwrap()
	for link in soup.select("a"):
		link.insert_after(link["href"])
		link.decompose()
	text = map(lambda a: a.strip(), soup.get_text().strip().split("\n"))
	text = "\n".join(list(text))
	text = re.sub("https?://([^/]+)/(@[^ ]+)", r"\2@\1", text) #put mentions back in
	text = re.sub("^@[^@]+@[^ ]+ *", r"", text) #...but remove the initial one
	text = text.lower() #for easier matching
	return text

known_toots = open('known_toots.txt', 'w+')
class ReplyListener(mastodon.StreamListener):
	def on_notification(self, notification):
		if notification['type'] == 'mention':
			acct = "@" + notification['account']['acct']
			post_id = notification['status']['id']
			mention = extract_toot(notification['status']['content'])
			toot = create.make_toot(True)['toot']
			compat = re.match("^compatibility check: (@[^@]+@[^ ]+) (?:and|&) (@[^@]+@[^ ]+)", mention)
			print(mention)
			#special functions
			if mention.startswith("yes or no:"):
				replies = ["yes", "nope", "no", "definitely!", "of course!", "no way.",
				"um, i don't actually know!", "i mean, i guess...", "sure!", "nah.",
				"maybe.", "i think you know the answer.", "yeah it's not looking good.",
				"probably.", "sure!", "heck no!"]
				toot = random.choice(replies)
			elif mention.startswith("override: "):
				#mistress wants direct control <3
				if acct not in ["@lynnesbian@deadinsi.de", "@00dani@vulpine.club"]:
					toot = "Insufficient privileges. This action has been reported to @lynnesbian@deadinsi.de."
				else:
					command = mention[len("override: "):]
					swaps = {
						"you": "i",
						"i are": "you are",
						"your": "my",
						"you're": "i'm",
						"yours": "mine",
					}
					gross_hack = "///DON'T_USE_THIS_PHRASE_IN_A_TOOT///"
					command = re.sub("\\bme\\b", "i", command)
					for one, two in swaps.items():
						command = re.sub("\\b{}\\b".format(one), gross_hack, command)
						command = re.sub("\\b{}\\b".format(two), one, command)
						command = re.sub(gross_hack, two, command)

					toot = command
			elif "apologise" in mention:
				apologies = ["please forgive me!", "i'm so sorry!", "sorry!",
				"my mistake!", "i'm always trying to do better!",
				"i'm sorry, i didn't mean it!", "sorry...", "oh, sorry..."]
				if acct == "@lynnesbian@deadinsi.de":
					apologies = ["f-forgive me, mistress!",
					"i'm so sorry, mistress!", "mistress lynne! i'm so sorry for this!",
					"i'm so sorry... y-you can punish me if you want...",
					"am i going to get punished for this? 0////0",
					"i've been a naughty bot... do i need punishment?",
					"lynne, i am not worthy of your love!",
					"mistress lynne, i cannot express my regret... how can i make this up to you?",
					"from the bottom of my heart, i apologise, mistress!",
					"no, no, no! how could i have let this happen in front of mistress?!",
					"m-maybe you'll have to punish me..."]
				toot = random.choice(apologies)
			elif compat != None:
				# toot = "{} and {} are {}% compatible.".format(compat.group(1), compat.group(2), random.randint(0,100))
				toot = "Feature disabled"
			toot = acct + " " + toot
			if acct == "@lynnesbian@deadinsi.de":
				prefixes = ["h-hello, mistress...", "hi lynne!",
				"(omg, mistress is talking to me!)", "m-mistress!", "lynne!",
				"hello, my favourite lesbian!", "hey lynne~"]
				if random.randint(1,5) == 3:
					toot = random.choice(prefixes) + " " + toot
			if acct == "@lynnesbian@deadinsi.de":
				if random.randint(1,1000) == 666:
					toot = "@lynnesbian@deadinsi.de i love you " * random.randint(10, 20)
			client.status_post(toot, post_id, visibility=notification['status']['visibility'])

rl = ReplyListener()
client.stream_user(rl)
