#!/usr/bin/env python3

import requests
import datetime

import django
django.setup()
from django.db import models
from gambitapp.models import GuardianId,GuardianClass

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
guardian_class_list = []

def getGuardianName(gid):
    name = GuardianId.objects.filter(guardianId=gid).values('guardianName')
    return name[0]['guardianName']

def getGuardianId(name):
    gid = GuardianId.objects.filter(guardianName=name).values('guardianId')
    return gid[0]['guardianId']

for g in GuardianId.objects.filter(active=1).values('guardianId'):
    guardian_list.append(g['guardianId'])

for c in GuardianClass.objects.all().values('guardianClassId'):
    print(c)
    guardian_class_list.append(c['guardianClassId'])

print(datetime.datetime.now())

#print(guardian_list)

#Lookup all active userIds per clan roster
#Then look up their three guardians and add them to the db
for membershipId in guardian_list:
    destinyMembershipId = membershipId
    profile_url = bungie_url + '/Destiny2/' + membershipType + '/Profile/' + str(membershipId) + '/?components=Characters'
    profile = requests.get(profile_url, headers=HEADERS)
    print(getGuardianName(membershipId))
    if profile.json()['ErrorCode'] != 1601:
        for characterId in profile.json()['Response']['characters']['data']:
            if int(characterId) in guardian_class_list:
                print(f'Character {characterId} for {getGuardianName(membershipId)} already added')
            else:
                guardianStatus = {}
                guardianStatus.update({'guardianId': membershipId})
                guardianStatus.update({'guardianClass': profile.json()['Response']['characters']['data'][characterId]['classType']})
                guardianStatus.update({'guardianClassId': characterId})
                print(guardianStatus)
                statsData = GuardianClass(**guardianStatus)
                statsData.save()
                print(f'New class for {getGuardianName(membershipId)} found. Adding {characterId}')