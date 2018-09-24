#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import mastodon
import os
import create

api_base_url = "https://botsin.space"
client = mastodon.Mastodon(
        client_id="clientcred.secret", 
        access_token="usercred.secret", 
        api_base_url=api_base_url)

known_toots = open('known_toots.txt', 'w+')
class ReplyListener(mastodon.StreamListener):
	def on_notification(self, notification):
		if notification['type'] == 'mention':
			acct = "@" + notification['account']['acct']
			post_id = notification['status']['id']
			toot = acct + " " + create.make_toot(True)['toot']
			client.status_post(toot, post_id, visibility='unlisted')

rl = ReplyListener()
client.stream_user(rl)
