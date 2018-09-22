#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mastodon import Mastodon
import sqlite3

api_base_url = "https://botsin.space"
client = Mastodon(
        client_id="clientcred.secret", 
        access_token="usercred.secret", 
        api_base_url=api_base_url)

#download all notifications and extract mentions
notifs = client.notifications()
print(len(notifs))
mentions = []

for notif in notifs:
	if notif['type'] == 'mention':
		#this is a mention
		mentions.append(notif)

print(mentions[0]['status'])