#!/usr/bin/env python3

import requests
import pprint
import datetime

from APIKEY import APIKEY
HEADERS = APIKEY
pp = pprint.PrettyPrinter(indent=2)

groupType='1'
groupName='BreakfastClubGaming'
groupId='1669746'
membershipType='1'
displayName='DigiCub'
bungie_url='https://www.bungie.net/Platform'
clanIds = {}
cid = []

def className(classId):
    if classId == 0:
        classType = 'Titan'
    elif classId == 1:
        classType = 'Hunter'
    else:
        classType = 'Warlock'
    return classType

print(datetime.datetime.now())

groupMembers_url = bungie_url + f'/GroupV2/{groupId}/Members/'
groupMembers = requests.get(groupMembers_url, headers=HEADERS)
for member in groupMembers.json()['Response']['results']:
    clanIds.update( {member['destinyUserInfo']['displayName']: member['destinyUserInfo']['membershipId']} )

for name,membershipId in clanIds.items():
#    print(name,membershipId)
    destinyMembershipId = membershipId
    profile_url = bungie_url + '/Destiny2/' + membershipType + '/Profile/' + membershipId + '/?components=Characters'
    try:
        profile = requests.get(profile_url, headers=HEADERS)
        if profile.json()['ErrorCode'] != 1601:
            cid = []
            for c_data in profile.json()['Response']['characters']['data']:
                cid.append(profile.json()['Response']['characters']['data'][c_data]['characterId'])
            print(f'Motes Lost for {name}')
#        print(cid)
#        pp.pprint(profile.json())
            for characterId in cid:
           # print(characterId +  str(profile.json()['Response']['characters']['data'][characterId]['classType']))
                classId = className(profile.json()['Response']['characters']['data'][characterId]['classType'])
                activity_url = bungie_url + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/?mode=63&count=100'
                try:
                    activity = requests.get(activity_url, headers=HEADERS)
                except:
                    print('Error ?')
                    continue
                if activity.json()['Response']:
                    motesLost = 0
                    for instance in activity.json()['Response']['activities']:
                        activityId = instance['activityDetails']['instanceId']
                        carnage_url = bungie_url + f'/Destiny2/Stats/PostGameCarnageReport/{activityId}/'
                        try:
                            carnage = requests.get(carnage_url, headers=HEADERS)
                            for char in carnage.json()['Response']['entries']:
                                if char['characterId'] == characterId:
                                    motesLost = motesLost + int(char['extended']['values']['motesLost']['basic']['displayValue'])
                                    #print(motesLost)
                        except:
                            print('Get Carnage Error')
                            continue

                else:
                    motesLost = 'No Gambit data found'
                print(f'\t{classId} : {motesLost}')
        else:
            print(f'No User Data found for {name}')
    except:
        print('Profile Lookup Error')
        continue
print(datetime.datetime.now())
