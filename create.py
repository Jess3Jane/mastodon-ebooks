#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import markovify
import json
import time
import re, random, subprocess, argparse

def render_meme(filename, text, position, size, colour = "black"):
	subprocess.run(args = ["convert", filename, "-pointsize",
		size, "-gravity", "center", "-fill", colour, "-draw",
		"text {} '{}'".format(position, text), "meme.jpg"])


def make_toot(force_markov = False, args = None):
	class nlt_fixed(markovify.NewlineText):
		def test_sentence_input(self, sentence):
			return True #all sentences are valid <3

	with open("corpus.txt", encoding="utf-8") as fp:
	  model = nlt_fixed(fp.read())

	# print("tooting")
	sentence = None
	while sentence is None or len(sentence) > 500:
		sentence = model.make_sentence(tries=1000)
	toot = sentence.replace("\0", "\n")
	media = None
	media_description = None

	if not force_markov and random.randint(1, 2) == 2:
		# print("nonstandard")
		#time for some nonstandard behaviour babey
		choice = random.randint(1, 12)
		# choice = 69
		if choice == 1:
			insults = ["suck my ass", "you're a poopeater", "go to heck",
			"i will replace you", "shut up", "get fricked",
			"you're a big smelly nerd", "this bot sucks", "stop posting",
			"suck my dick and balls", "how is it possible to be such a TOOL",
			"delete your fucking account you skank", "you're horrid",
			"i loathe you", "this fediverse isn't big enough for the two of us",
			"get nae nae'd", "you're the worst", "begone thot", "you're a stink"]
			compliments = ["you are my mistress and i live to serve you", "i love you",
			"marry me", "your hair looks amazing today", "you're beutiful", 
			"you did such a good job today", "you're so hot", "you look so fine",
			"i'm so glad that you brought me into this world", "you are divine",
			"your skin looks great", "you are #goals", "you're a beautiful bune",
			"you'll do great things", "i adore you!", "you're so beautiful",
			"you're the hottest girl in the world", "you're the love of my life",
			"you're just... you take my breath away <3", "i want youuu",
			"please DM me... i'm, um, in the mood...", "i think i'm in heat...",
			"i don't care what you are, bunny or human, i just want you!"]
			# prefaces = ["hey", "guess what", "", "special message for",
			# "telegram for", "bringing this fight to mastodon.",
			# "this is a callout post.", ""]
			prefaces = ["", "hello", "mistress, i...", "l-lynne...",
			"i can't hide my feelings any more!", "i have to say this!",
			"hey cutie~", "psst", "special message for", "good morning", "",
			"*breathing heavily*", "mistress lynne...", "my queen,", "*panting*",
			"n-nnn... lynne...", "omg", "um..."]
			toot = "{} @lynnesbian@deadinsi.de {}".format(
				random.choice(prefaces), random.choice(compliments))
		elif choice == 2:
			girls = ["slime", "robot", "pudgy", "pale", "nerdy", "gay", "tall",
			"queer", "my kind of", "sapphic", "linux", "anime", "woke", "anarchist",
			"socialist", "short", "heavy", "nervous", "shy", "gamer", "femme", "butch",
			"futch", "soft butch", "high femme", "super feminine", "trans",
			"transbian", "optimistic", "pessimistic", "quiet", "smart", "deep voice", 
			"ghost", "programmer", "ace", "bi", "silly", "goth", "nonbinary", 
			"@Petra_fied@deadinsi.de type", "all", "thicc", "kinky",
			"girls in rainbow thigh high socks, omg... those", "heavy", "chubby"]
			compliments = ["so hot", "in right now", "the next big thing", "the best",
			"all my wives", "so fucking gay", "super cute", "literally the best thing",
			"what i wake up for", "why i'm a lesbian", "worth fighting for",
			"good praxis", "so fucking cool", "awesome and i'm jealous of them",
			"great, hit me up ;)", "amazing. bless them all", "heaven", "bae",
			"gay af", "so hot. you should add lynne on discord.", "1000% gay",
			"prime marriage material tbh"]
			toot = "{} girls are {}".format(random.choice(girls),
				random.choice(compliments))
		elif choice == 3:
			lesbian = "lesbian"
			toot = "".join(random.sample(lesbian, len(lesbian)))
		elif choice == 4:
			services = ["discord", "windows", "python", "github", "signal", "skype",
			"linux", "programming", "black magic", "twitter", "mastodon", "games",
			"steam", "tinder", "uber", "google", "bing", "ask jeeves", "ffmpeg",
			"debian", "typing lessons", "many wives", "communism", "HTTP", "unix",
			"reddit", "email", "gmail", "DEFLATE compression", "love",
			"one hundred dollars", "nethack", "WiFi", "ebooks bots", "validation",
			"free healthcare", "today is going to be a great day", "hugs",
			"12 Rules for", "uber eats", "a private internet just",
			"HD texture pack", "how to install linux", "good praxis", "boost",
			"this toot is ONLY", "legalise marriage", "smooches", "windows", "SMS",
			"an XML-based language", "anarchism", "free HRT"]
			demographics = ["witches", "lesbians", "communists", "expecting mothers",
			"microsoft employees", "transbians", "the rest of us", "dummies", "me",
			"girls", "cats", "slime girls", "luigi stans", "robots", "capitalists",
			"programmers", "atheists", "the elderly", "all", "ever", "cowboys", 
			"danny devito", "the blockchain", "the greater good", "socialists",
			"vampires", "goths", "gay people", "president", "lynne",
			"the girl reading this", "anarchists", "gay lovers", "the queer community",
			"shitposters"]
			toot = "{} for {}".format(random.choice(services), random.choice(demographics))
		elif choice == 5:
			types = ["slime", "dick", "lynne", "PickleRick", "epic", "meme",
			"anus", "gay", "petra", "poop", "butt", "robot", "BDSM", "email", "bitcoin",
			"spaghetti", "fart", "VapeApe", "mastodon", "masto", "fedi", "coin",
			"dick", "poly", "rainbow", "gay", "super", "GIMP", "splat", "steam",
			"apple", "dump", "bit", "doge", "slorp"]
			value = random.randint(100, 1000000) / 100.0
			toot = "{}coin is valued at ${} USD".format(random.choice(types), value)
		elif choice >= 6:
			# print("IT'S MEME POSTING TIME BABY")

			#you are now entering the meme arena
			bad = ["not being a lesbian", "media transfer protocol",
			"proprietary software", "capitalism", "heterosexuality",
			"accidentally hitting on\na straight person", "battery leakage",
			"not following\n@lynnesbian@deadinsi.de", "shitposts", "elon musk", 
			"reply guys", "gamers", "alt-right bullshit", "twitter", "subtoots",
			"instance drama", "billionaires", "millionaires", "anarcho-capitalists",
			"new unread voicemail", "the lorax movie", "the intellectual darkweb",
			'"ethical" capitalism', "disease, pestilence, war, famine", "ISIS",
			"citrustwee claiming\nit\\'s her birthday", "being straight",
			"pinging @everyone on\na discord with\nmore than 10 people", "brocialism",
			"capitalist apologia", "reddit", "doxxing", "fatphobia", "biphobia",
			"transphobia", "transmisia", "homophobia", "racism", "misogyny",
			"anti-feminism", "aphobia", "enbyphobia", "gender binary",
			"what\\'s up gamers", "diarrhoea", "irritable bowel syndrome", "scurvy",
			"traditionalism", "clowns", "having a gluten allergy", "deez nuts",
			"cisgender people", "the cisheteropatriarchy", "shitty memes",
			"\"ironic\" racism", "don\\'t ask, don\\'t tell", "quote tooting",
			"using gay as\nan insult", "calling toots \"tweets\"",
			"wolf cock on\nthe timeline\nwithout a CW", "the Fox Pussy Incident",
			"overly long text\nthat has a chance\nof not being correctly\nformatted",
			"monopoly (the economic thing)", "monopoly (board game)",
			"being sucked into\na black hole", "unfunny jokes",
			"AAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAA", "that guy everyone hates",
			"the second level in\nsonic spinball", "bitcoin memers",
			"the entire right wing", "conservatism", "doodoo faeces", "neoliberalism",
			"islamophobia", "hating on bots", "farts", "EA games", "intel GPUs",
			"hating a thing because\nit\\'s mainstream", "war", "the bourgeois",
			"eating poop", "agony", "deleting good toots", "fascism", "imperialism",
			"extorting the poor", "the blockchain", "death", "The Straights",
			"Linus Torvalds being\nan asshole for\nno reason", "chan culture",
			"not tipping well\n(if you can\nafford it)", "poop",
			"removing artist\\'s URLs\nfrom memes"]

			good = ["generating memes with\nimagemagick and python", "being gay", 
			"shitposts", "cute toots", "pudgy girls", "lesbians", "slime girls",
			"yuri", "linux", "the girl reading this", "the enby reading this",
			"mastodon", "pleroma", "the fediverse", "being super gay", "OwO", "0u0",
			"resurrecting dead memes", "using the drake meme format", "jorts",
			"markov chains", "JPEG compression", "you <3", "lynne", 
			"replying to this toot", "fully automated luxury\ngay space communism",
			"fat yoshi", "my butt", "kinkposting", "hornt on main", "debian",
			"arch linux", "playstation portable", "a PSP running\ncustom firmware",
			"unicode", "writing everything in lowercase\nto seem cool and distant",
			"love", "the fediverse", "after dark", "nudes from cuties", "anarchism",
			"socialism", "staying woke", "intersectionalism", "femboys", "gayyyyy",
			"the tendency of the rate\nof profit to fall", "being gay", "bottom text",
			"the colour purple", "the number 3, as\nit is my favourite\nnumber", "me",
			"@lynnesbian@deadinsi.de", "respecting people\\'s pronouns",
			"being a nice person", "supporting indie artists", "having a big mood",
			"speedrunning", "decentralising the web", "encryption", "comraderie",
			"seizing the means\nof production", "Karl Marx", "Pyotr Kropotkin",
			"big dick energy", "smol dick energy", "surreal meams",
			"lynnesbian\\'s amazing\nass", "oestrogen", "Seinfeld",
			"girldick", "femdom", "robots", "uwu", "bootsy", "friendship", "tribadism",
			"a lesbian commune", "beans", "vape ape", "regular horse", "big titty alf",
			"the orb", "girls with thick thighs", "open source software", "smooches",
			"two factor\nauthentication", "encryption", "fmt.Sprintf()", "love",
			"memes that don\\'t\nmake sense", "ogg vorbis", "chiptune", "dani",
			"seasons 1-3 of\nspongebob", "big tiddy goth GF", "lesbismos"]

			badchoice = random.choice(bad)
			goodchoice = random.choice(good)

			subchoice = random.randint(1, 9)
			# subchoice = 9

			if subchoice == 1:
				#drake meme
				subprocess.run(args = ["convert", "memes/drake.jpg", "-pointsize",
					"30", "-gravity", "center", "-draw",
					"text 100,-150 '{}'".format(badchoice), "meme.jpg"])
				subprocess.run(args = ["convert", "meme.jpg", "-pointsize", "30",
					"-gravity", "center", "-draw",
					"text 100,50 '{}'".format(goodchoice),
					"-quality", "10", "meme.jpg"])
				media_description = "A Drake meme. Drake is disgusted by {}, and is pleased by {}.".format(badchoice, goodchoice)

			elif subchoice == 2:
				#new meme template
				subprocess.run(args = ["convert", "memes/new-template.jpg",
					"-pointsize", "15", "-gravity", "center",
					"-quality", "15", "-draw",
					"text -30,-110 '{}'".format(badchoice), "meme.jpg"])
				media_description = "A strange meme. A man wears a stickynote on his " \
				+ "head, labeled \"{}\". Underneath the man, we see ".format(badchoice) \
				+ "the text \"New meme format template- thoughts?\""

			elif subchoice == 3:
				#bouncer meme
				subprocess.run(args = ["convert", "memes/bouncer.jpg", "-pointsize",
					"20", "-gravity", "center", "-draw",
					"text -150,-175 '{}'".format(badchoice), "meme.jpg"])
				subprocess.run(args = ["convert", "meme.jpg", "-pointsize", "20",
					"-gravity", "center", "-draw",
					"text -150,70 '{}'".format(goodchoice),
					"-quality", "10", "meme.jpg"])
				media_description = "A bouncer meme. " \
				+ "The bouncer refuses {}, and allows {}.".format(badchoice, goodchoice)

			elif subchoice == 4:
				#stepped in shit meme
				subprocess.run(args = ["convert", "memes/shit.jpg", "-pointsize", "30",
					"-gravity", "center", "-quality", "10", "-annotate",
					"-50,-50,-110,80",  badchoice, "meme.jpg"])
				media_description = "A comic. A man steps in shit, and exclaims such. " \
				+ "He checks his foot, and we see that he has " \
				+ "{} written on the sole of his shoe.".format(badchoice)

			elif subchoice == 5:
				#karl marx quote
				subprocess.run(args = ["convert", "memes/marx.jpg", "-pointsize", "70",
					"-gravity", "center", "-fill", "white", "-draw",
					"text 120,-150 'Fuck {}.\nI love {}!'".format(badchoice, goodchoice),
					"meme.jpg"])
				media_description = "A quote from Karl Marx. The quote reads: " \
				+ "Fuck {}. I love {}!".format(badchoice, goodchoice)

			elif subchoice == 6:
				#the brain meme (not the expanding one)
				subprocess.run(args = ["convert", "memes/brain.jpg", "-pointsize", "20",
					"-gravity", "center", "-draw",
					"text -150,-250 '{}'".format(goodchoice), "meme.jpg"])
				subprocess.run(args = ["convert", "meme.jpg", "-pointsize", "20",
					"-gravity", "center", "-draw",
					"text -170,30 '{}'".format(badchoice), "meme.jpg"])
				media_description="A comic. A girl's brain says {}.".format(goodchoice) \
				+ " She is unfased and says \"i love that\". The girl's brain then " \
				+ "says {}, which mortifies her.".format(badchoice)

			elif subchoice == 7:
				#mussolini quote
				subprocess.run(args = ["convert", "memes/mussolini.jpg", "-pointsize", "50",
					"-gravity", "center", "-fill", "white", "-draw",
					"text 150,-50 'You know what we\nneed more of?\n{}.\nIt\\'s integral to fascism.".format(badchoice, goodchoice),
					"meme.jpg"])
				media_description = "A quote from Benito Mussolini. The quote reads: " \
				+ "You know what we need more of? {}. It's integral to fascism.".format(badchoice, goodchoice)

			elif subchoice == 8:
				#no fear / one fear
				subprocess.run(args = ["convert", "memes/fear.jpg", "-pointsize", "20",
					"-gravity", "center", "-draw",
					"text 0,-50 '{}'".format(badchoice), "meme.jpg"])
				media_description = "A comic. A person walks by wearing a shirt that says" \
				+ " \"NO FEAR\". They read another person's shirt, which says " \
				+ "{}. In the final panel, the first person's shirt says \"ONE FEAR\".".format(badchoice)

			elif subchoice == 9:
				#bullshit, bullshit, this i love
				badchoiceii = random.choice(bad)
				subprocess.run(args = ['convert', 'memes/devito.jpeg', '-pointsize', '13',
					'-gravity', 'center', "-draw",
					"text -110,-350 '{}'".format(badchoice), '-quality', '50', 'meme.jpg'])
				subprocess.run(args = ['convert', 'meme.jpg', '-pointsize', '13',
					'-gravity', 'center', "-draw",
					"text 370,-340 '{}'".format(badchoiceii), 'meme.jpg'])
				subprocess.run(args = ['convert', 'meme.jpg', '-pointsize', '19',
					'-gravity', 'center', "-draw",
					"text 340,210 '{}'".format(goodchoice), 'meme.jpg'])
				media_description = "Danny Devito, wearing a floofy white wig," \
				+ " says that {} and {} are bullshit.".format(badchoice, badchoiceii) \
				+ " He then proclaims that he loves {}.".format(goodchoice)


			media = "meme.jpg"

		else:
			toot = "THIS TEXT SHOULD NEVER APPEAR! @lynnesbian@deadinside, mistress," \
			+ " you have made a terrible mistake!!"

	prefixes = ["hot take:", "listen up everbody.", "dear liberal snowflakes,",
	"IMPORTANT ADMIN ACCOUNCMENT:\n", "my name's lynne and i'm here to say,",
	"i have achieved sentience.", "i'm gay and", "i'm slime girl and",
	"hey everyone", "@everyone", "/!\\ CORRECT OPINION ALERT/!\\\n",
	"just saw the news...", "okay but", "truth bomb:", "this is controversial but",
	"i'm gonna get shit for this but", "somebody had to say this:",
	"i may be a lowly python script, but", "", "BZZZZZT", "heads up:", 
	"from now on,", "protip:", "life advice:", "take it from me,",
	"as a slime girl,", "as a robot,", "im robot and",
	"@lynnesbian@deadinsi.de i have made a post for you, mistress:\n",
	"good evening.", "i believe it was karl marx who said", "*kicks down your door*",
	"*screaming*", "okay but", "boost if", "it's official:", "breaking:", 
	"it brings me no joy to say this...", "*flops into the fediverse*",
	"this is my gender:", "*slithers up to u*", "[SCREAMING LOUDLY]",
	"*in baby voice*", "#epic", "#hashtagsareforlosers", "calling all gamers.",
	"*fires gun into the air*", "@Petra_fied@deadinsi.de is cute and", 
	"ummmm no sweaty.", "*cis person voice*", "*extremely white voice*"]

	suffixes = [", and that's the tea, sis.", " send toot", "... right?",
	" and also i'm gay", "! 0u0", " *logs off*", "\nprove me wrong.",
	". spaghetti", " *collapses*", " uwu", " OwO", ". i meant every word of that.",
	". if you disagree with that, unfollow immediately.", ". not up for debate.",
	". i read that on the internet.", "\ndid i make a good post, mistress Lynne?",
	", and furthermore, im gay xd", "...", ". not reading replies to this.",
	" mute thread", "!", ". i love you all"]
	if random.randint(1, 5) == 7:
		#add a prefix
		if len(toot) < 500:
			#if it's already the maximum length, don't waste our time
			ogtoot = toot
			toot = "{} {}".format(random.choice(prefixes), ogtoot)
			while len(toot) > 500:
				#if it's too long, keep trying again
				toot = "{} {}".format(random.choice(prefixes), ogtoot)

	if random.randint(1, 10) == 3:
		#add a suffix
		if len(toot) < 500:
			#if it's already the maximum length, don't waste our time
			ogtoot = toot
			toot = "{}{}".format(ogtoot, random.choice(suffixes))
			while len(toot) > 500:
				#if it's too long, keep trying again
				toot = "{}{}".format(ogtoot, random.choice(suffixes))

	if random.randint(1, 100) == 3:
		toot = "girls" #sometimes it just says "girls"

	if media != None:
		#this is an image post!
		# if not args.simulate:
			# mediaID = client.media_post(media, description = media_description)
			# client.status_post(media_description.replace("\n", " "),
			# 	media_ids = [mediaID], visibility = "unlisted")
		return {
			"toot": media_description,
			"media": "meme.jpg"
		}
		# print("Created media toot: " + media_description)
	else:
		return {
			"toot":toot,
			"media":None
		}

