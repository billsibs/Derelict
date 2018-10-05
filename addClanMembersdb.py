#!/usr/bin/env python3

import requests
import datetime

import django
django.setup()
from django.db import models
from gambitapp.models import GuardianId

from APIKEY import APIKEY
HEADERS = APIKEY

import pprint
pp = pprint.PrettyPrinter(indent=2)

groupType='1'
groupId='1669746'
membershipType='1'
bungie_url='https://www.bungie.net/Platform'
clanIds = {}
cid = []
guardian_list = []

#savedGuardians = GuardianId.objects.all().values('guardianId')
#guardians_list = list(savedGuardians['guardianId'])
#print(guardians_list[0]['guardianId'])

for g in GuardianId.objects.all().values('guardianId'):
    guardian_list.append(g['guardianId'])


print(datetime.datetime.now())

groupMembers_url = bungie_url + f'/GroupV2/{groupId}/Members/'
groupMembers = requests.get(groupMembers_url, headers=HEADERS)
for member in groupMembers.json()['Response']['results']:
    clanIds.update( {member['destinyUserInfo']['displayName']: member['destinyUserInfo']['membershipId']} )

print(guardian_list)

#Lookup all guardianIds per clan roster
for name,membershipId in clanIds.items():
    if int(membershipId) in guardian_list:
        print(f'{name} found. Doing Nothing')
    else:
        print(f'{name} not found. Time to get busy')
        guardianStatus = {}
        destinyMembershipId = membershipId
        profile_url = bungie_url + '/Destiny2/' + membershipType + '/Profile/' + membershipId + '/?components=Characters'
        profile = requests.get(profile_url, headers=HEADERS)
        #Error 1601 = Not Found. Ignore accounts with no guardians (how is that possible?)
        if profile.json()['ErrorCode'] != 1601:
            gActive = 1
        else:
            gActive = 0
        guardianStatus.update({'guardianName': name} )
        guardianStatus.update({'guardianId' : membershipId})
        guardianStatus.update({'active' : gActive})
#Debug        print(guardianStatus)
        statsData = GuardianId(**guardianStatus)
        statsData.save()