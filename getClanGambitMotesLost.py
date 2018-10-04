#!/usr/bin/env python3

import requests
import datetime

#Formatting if needing to view json in an easier to read output
import pprint
pp = pprint.PrettyPrinter(indent=2)

#Read in API key from separate file. Keep it secret.
from bungie_apikey import APIKEY
HEADERS = APIKEY

groupType='1'
groupName='BreakfastClubGaming'
groupId='1669746'
membershipType='1'
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

#Begin
print(datetime.datetime.now())

#Look up all guardians in clan
groupMembers_url = bungie_url + f'/GroupV2/{groupId}/Members/'
groupMembers = requests.get(groupMembers_url, headers=HEADERS)
for member in groupMembers.json()['Response']['results']:
    clanIds.update( {member['destinyUserInfo']['displayName']: member['destinyUserInfo']['membershipId']} )

#Lookup all guardianIds per clan roster
for name,membershipId in clanIds.items():
    destinyMembershipId = membershipId
    profile_url = bungie_url + '/Destiny2/' + membershipType + '/Profile/' + membershipId + '/?components=Characters'
    try: #If error occurs, look up next set of guardians
        profile = requests.get(profile_url, headers=HEADERS)
        #Error 1601 = Not Found. Ignore accounts with no guardians (how is that possible?)
        if profile.json()['ErrorCode'] != 1601:
            cid = []
            for c_data in profile.json()['Response']['characters']['data']:
                cid.append(profile.json()['Response']['characters']['data'][c_data]['characterId'])
            print(f'Motes Lost for {name}')
            #Gather carnage reports for each guardian class
            for characterId in cid:
                classId = className(profile.json()['Response']['characters']['data'][characterId]['classType'])
                activity_url = bungie_url + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/?mode=63&count=100'
                try: #If error occurs, move on to next class 
                    activity = requests.get(activity_url, headers=HEADERS)
                except:
                    print('Activity lookup Error')
                    continue
                #Check and see if gambit data exists, otherwise tell no gambit data found
                if activity.json()['Response']:
                    motesLost = 0
                    for instance in activity.json()['Response']['activities']:
                        activityId = instance['activityDetails']['instanceId']
                        carnage_url = bungie_url + f'/Destiny2/Stats/PostGameCarnageReport/{activityId}/'
                        try: #If error occurs, move on to next match for carnage report
                            carnage = requests.get(carnage_url, headers=HEADERS)
                            for char in carnage.json()['Response']['entries']:
                                if char['characterId'] == characterId:
                                    motesLost = motesLost + int(char['extended']['values']['motesLost']['basic']['displayValue'])
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
