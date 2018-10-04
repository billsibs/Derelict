#!/usr/bin/env python3

import requests
import datetime
import sys

#Formatting if needing to view json in an easier to read output
import pprint
pp = pprint.PrettyPrinter(indent=2)

#Read in API key from separate file. Keep it secret.
from bungie_apikey import APIKEY
HEADERS = APIKEY

#Class to translate Guardian Class Id to text
def className(classId):
    if classId == 0:
        classType = 'Titan'
    elif classId == 1:
        classType = 'Hunter'
    else:
        classType = 'Warlock'
    return classType

membershipType='1'
displayName=sys.argv[1]
bungie_url='https://www.bungie.net/Platform'
motesLost = 0
cid = [] #characterId
clanIds = {}

#Begin
print(datetime.datetime.now())

#Look Up accountId based on XBL Name
search_url= bungie_url + '/Destiny2/SearchDestinyPlayer/' + membershipType + '/' + displayName + '/'
res = requests.get(search_url, headers=HEADERS)
membershipId = res.json()['Response'][0]['membershipId']
#Dual variables used for membershipId. Create duplicate variables
destinyMembershipId = membershipId

#Look Up Guardians based on membershipId
profile_url = bungie_url + '/Destiny2/' + membershipType + '/Profile/' + membershipId + '/?components=Characters'
profile = requests.get(profile_url, headers=HEADERS)
for c_data in profile.json()['Response']['characters']['data']:
    cid.append(profile.json()['Response']['characters']['data'][c_data]['characterId'])

#For each guardianId, look up their last 100 post carnage matches
for characterId in cid:
    classId = className(profile.json()['Response']['characters']['data'][characterId]['classType'])
    activity_url = bungie_url + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/?mode=63&count=100'
    activity = requests.get(activity_url, headers=HEADERS)
#If there is a response in activity, look up stats, otherwise do nothing and return 0
    if activity.json()['Response']:
        motesLost = 0
        for instance in activity.json()['Response']['activities']:
            activityId = instance['activityDetails']['instanceId']
            carnage_url = bungie_url + f'/Destiny2/Stats/PostGameCarnageReport/{activityId}/'
            carnage = requests.get(carnage_url, headers=HEADERS)
            for char in carnage.json()['Response']['entries']:
                if char['characterId'] == characterId:
                    motesLost = motesLost + int(char['extended']['values']['motesLost']['basic']['displayValue'])
    #Do nothing (Return text) if no activity found.
    else:
        motesLost = 'No Gambit data found'
    print(f'\tMotes Lost for {classId} : {motesLost}')

#End Run
print(datetime.datetime.now())

#Error stats of json call. USed for debug
#error_stat = res.json()['ErrorStatus']
#print("Error status: " + error_stat + "\n")
