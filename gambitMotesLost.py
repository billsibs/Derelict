#!/usr/bin/env python3

import requests
import pprint
import datetime
import sys

from APIKEY import APIKEY
pp = pprint.PrettyPrinter(indent=2)
HEADERS = APIKEY

def className(classId):
    print(classId)
    if classId == 0:
        classType = 'Titan'
    elif classId == 1:
        classType = 'Hunter'
    else:
        classType = 'Warlock'
    return classType

groupType='1'
groupName='BreakfastClubGaming'
groupId='1669746'
membershipType='1'
displayName=sys.argv[1]
bungie_url='https://www.bungie.net/Platform'
motesLost = 0
cid = [] #characterId
clanIds = {}
print(datetime.datetime.now())

groupMembers_url = bungie_url + f'/GroupV2/{groupId}/Members/'
groupMembers = requests.get(groupMembers_url, headers=HEADERS)
for member in groupMembers.json()['Response']['results']:
    clanIds.update({member['destinyUserInfo']['displayName'], member['destinyUserInfo']['membershipId']})
    displayName = member['destinyUserInfo']['displayName']
    meId = member['destinyUserInfo']['membershipId']
    print(f'{name} : {meId}')




search_url= bungie_url + '/Destiny2/SearchDestinyPlayer/' + membershipType + '/' + displayName + '/'
res = requests.get(search_url, headers=HEADERS)

membershipId = res.json()['Response'][0]['membershipId']
destinyMembershipId = membershipId

profile_url = bungie_url + '/Destiny2/' + membershipType + '/Profile/' + membershipId + '/?components=Characters'
profile = requests.get(profile_url, headers=HEADERS)

for c_data in profile.json()['Response']['characters']['data']:
    cid.append(profile.json()['Response']['characters']['data'][c_data]['characterId'])

for characterId in cid:
    classId = className(profile.json()['Response']['characters']['data'][characterId]['classType'])
    activity_url = bungie_url + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/?mode=63&count=100'
    activity = requests.get(activity_url, headers=HEADERS)
    if activity.json()['Response']:
        motesLost = 0
        for instance in activity.json()['Response']['activities']:
            activityId = instance['activityDetails']['instanceId']
            carnage_url = bungie_url + f'/Destiny2/Stats/PostGameCarnageReport/{activityId}/'
            carnage = requests.get(carnage_url, headers=HEADERS)
            for char in carnage.json()['Response']['entries']:
                if char['characterId'] == characterId:
                    motesLost = motesLost + int(char['extended']['values']['motesLost']['basic']['displayValue'])
    else:
        motesLost = 'No Gambit data found'
    print(f'\tMotes Lost for {classId} : {motesLost}')

print(datetime.datetime.now())

error_stat = res.json()['ErrorStatus']
print("Error status: " + error_stat + "\n")
