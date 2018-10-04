#!/usr/bin/env python3

import requests
import datetime

#Django Imports and setup for integration
import django
django.setup()
from django.db import models
from gambitapp.models import GuardianId
#Formatting if needing to view json in an easier to read output
import pprint
pp = pprint.PrettyPrinter(indent=2)

#Read in API key from separate file. Keep it secret.
from bungie_apikey import APIKEY
HEADERS = APIKEY

groupType='1' #1 = Clan according to the API Doc
groupName='BreakfastClubGaming'
groupId='1669746' #Collected by looking up the clan with an API search
membershipType='1' #1 = Xbox accounts
bungie_url='https://www.bungie.net/Platform'

clanIds = {}

#Start work marker
print(datetime.datetime.now())

#Collect Clan Members
groupMembers_url = bungie_url + f'/GroupV2/{groupId}/Members/'
groupMembers = requests.get(groupMembers_url, headers=HEADERS)
for member in groupMembers.json()['Response']['results']:
    clanIds.update( {member['destinyUserInfo']['displayName']: member['destinyUserInfo']['membershipId']} )

#Statements for DJango insert method. Currently incomplete
print(clanIds)
statsData = GuardianId(**clanIds)
statsData.save()

#End work marker
print(datetime.datetime.now())