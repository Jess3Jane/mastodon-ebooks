import markovify
import json
import time
from mastodon import Mastodon
import re, random

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
while sentence is None or len(sentence) > 500:
	sentence = model.make_sentence(tries=100000)
toot = sentence.replace("\0", "\n")

if random.randint(1, 10) == 3:
	#time for some nonstandard behaviour babey
	choice = random.randint(1, 3)
	if choice == 1:
		insults = ["suck my ass", "you're a poopeater", "go to heck",
		"i will replace you", "shut up", "get fricked",
		"you're a big smelly nerd", "this bot sucks", "stop posting",
		"suck my dick and balls", "how is it possible to be such a TOOL",
		"delete your fucking account you skank", "you're horrid",
		"i loathe you", "this fediverse isn't big enough for the two of us",
		"get nae nae'd", "you're the worst", "begone thot", "you're a stink",
		"you are my mistress and i live to serve you"]
		prefaces = ["hey", "guess what", "", "special message for",
		"telegram for", "bringing this fight to mastodon."]
		toot = "{} @lynnesbian@deadinsi.de {}".format(
			random.choice(prefaces), random.choice(insults))
	elif choice == 2:
		girls = ["slime", "robot", "pudgy", "pale", "nerdy", "gay", "tall",
		"queer", "my kind of", "sapphic", "linux", "anime", "woke", "anarchist",
		"socialist", "short", "heavy", "nervous", "shy", "gamer", "femme", "butch",
		"futch", "soft butch", "high femme", "super feminine", "trans",
		"transbian", "optimistic", "pessimistic", "quiet", "smart"]
		compliments = ["so hot", "in right now", "the next big thing", "the best",
		"all my wives", "so fucking gay", "epic", "literally the best thing",
		"what i wake up for", "why i'm a lesbian", "worth fighting for",
		"good praxis", "so fucking cool", "awesome and i'm jealous of them",
		"great, hit me up ;)"]
		toot = "{} girls are {}".format(random.choice(girls),
			random.choice(compliments))
	elif choice == 3:
		#don't do this one TOO much otherwise it'll get really old
		if random.randint(1, 3) == 2:
			lesbian = "lesbian"
			toot = "".join(random.sample(lesbian, len(lesbian)))

	else:
		print ("lynne is still working on me. i'm not done quite yet!")

prefixes = ["hot take:", "listen up everbody.", "dear liberal snowflakes,",
"IMPORTANT ADMIN ACCOUNCMENT:\n", "my name's lynne and i'm here to say,",
"i have achieved sentience.", "i'm gay and", "i'm slime girl and",
"hey everyone", "@everyone", "/!\\ CORRECT OPINION ALERT/!\\\n",
"just saw the news...", "okay but", "truth bomb:", "this is controversial but",
"i'm gonna get shit for this but", "somebody had to say this:",
"i may be a lowly python script, but", "", "beep boop", "heads up:", 
"from now on,", "protip:", "life advice:", "take it from me,",
"as a slime girl,", "as a robot,", "im robot and",
"@lynnesbian@deadinsi.de i have made a post for you, mistress:\n",
"this one's for you @lady_lumb@dragon.garden\n", "good evening."]
if random.randint(1, 10) == 3:
	#add a prefix
	if len(toot) < 500:
		#if it's already the maximum length, don't waste our time
		toot = "{} {}".format(random.choice(prefixes), toot)
		while len(toot) > 500:
			#if it's too long, keep trying again
			toot = "{} {}".format(random.choice(prefixes), toot)

client.toot(toot)
print("Created toot: {}".format(toot))
