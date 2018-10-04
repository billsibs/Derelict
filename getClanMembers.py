#!/usr/bin/env python3

import requests
import pprint
import datetime

import django
django.setup()
from django.db import models
from gambitapp.models import GuardianId




pp = pprint.PrettyPrinter(indent=2)
HEADERS = 

groupType='1'
groupName='BreakfastClubGaming'
groupId='1669746'
membershipType='1'
displayName='DigiCub'
bungie_url='https://www.bungie.net/Platform'
clanIds = {}
cid = []

print(datetime.datetime.now())

groupMembers_url = bungie_url + f'/GroupV2/{groupId}/Members/'
groupMembers = requests.get(groupMembers_url, headers=HEADERS)
for member in groupMembers.json()['Response']['results']:
    clanIds.update( {member['destinyUserInfo']['displayName']: member['destinyUserInfo']['membershipId']} )

print(clanIds)
statsData = GuardianId(**clanIds)
statsData.save()
