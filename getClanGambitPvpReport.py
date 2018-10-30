#!/usr/bin/env python3

import requests
import datetime
import json
import sys
import pprint
import django
django.setup()

from django.db import models

from gambitapp.models import gambitStats,GuardianId,gambitPVP

from apikeys import bungie
HEADERS = bungie.APIKEY

import bungotools

gambitColumns = []
medalsColumns = []
match_list = []
temp_list = []
guardian_list = []
insertData = {}
pp = pprint.PrettyPrinter(indent=2)

countLimit=200
groupType='1'
groupId='1669746'
membershipType='1'
bungie_url='https://www.bungie.net/Platform'

pvpstrings = [
#        'completionReason',
#        'standing',
#        'team',
        ]


guardian_list = bungotools.getdbListValues(GuardianId.objects.filter(active=1).values('guardianId'), 'guardianId')

#Get all unique matchIds from db
def getMatchList():
#    return sorted(set(gambitStats.objects.all().values('matchId'), 'matchId'))
    for m in gambitPVP.objects.all().values('matchId'):
        temp_list.append(m['matchId'])
    return sorted(set(temp_list))
#print(match_list)
def getGuardianName(gid):
    name = GuardianId.objects.filter(guardianId=gid).values('guardianName')
    return name[0]['guardianName']

for clanMember in guardian_list:
    membershipId = str(clanMember)
    destinyMembershipId = membershipId
    profile_url = bungie_url + '/Destiny2/' + membershipType + '/Profile/' + membershipId + '/?components=Characters'
    print(profile_url)
    try:
        #Gather Guardian IDs for member profile
        profile = requests.get(profile_url, headers=HEADERS)
        cid = []
        for c_data in profile.json()['Response']['characters']['data']:
                cid.append(profile.json()['Response']['characters']['data'][c_data]['characterId'])
    except Exception as e:
        print(f'Guardian Lookup Failed for Player:{getGuardianName(membershipId)}')
        if profile.json()['ErrorCode'] == 5:
            print(profile.json()['Message'])
            sys.exit(0)
        continue
    #For each Guardian class, get their list of match IDs
    for characterId in cid:
        gamefound=0
        gameadded=0
        gameexist=0
        activity_url = bungie_url + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/?mode=63&count={countLimit}'
        try: #If error occurs, move on to next class 
            activity = requests.get(activity_url, headers=HEADERS)
        except:
            print(f'Activity lookup Error for Player:{getGuardianName(membershipId)} Guardian:{characterId}')
            continue
        #Check and see if gambit data exists, otherwise tell no gambit data found
        if activity.json()['Response']:
#            print(activity.json())
            for instance in activity.json()['Response']['activities']:
                gamefound += 1
                if int(instance['activityDetails']['instanceId']) in getMatchList():
#                    print('Match Found. No need to add for ' + str(clanMember) )
                    gameexist += 1
                else:
#                    print('Match not found for ' + str(clanMember))
                    activityId = instance['activityDetails']['instanceId']
                    carnage_url = bungie_url + f'/Destiny2/Stats/PostGameCarnageReport/{activityId}/'
#                    print(carnage_url)
                    try:
                        carnage = requests.get(carnage_url, headers=HEADERS)
                        gameadded += 1
                        #pp.pprint(carnage.json())
                        for carnageData in carnage.json()['Response']['entries']:
                            insertData = {}
                            characterId = carnageData['characterId']
#                            print(f'Debug: {characterId}')
                            insertData.update( { 'guardianId': int(characterId) })
                            insertData.update( { 'matchId' : int(carnage.json()['Response']['activityDetails']['instanceId']) } )
                            insertData.update( { 'matchDate' : carnage.json()['Response']['period'] .split('T')[0] } )
#                            print(carnageData)
                            for data in carnageData['values']:
                                if 'medal' not in data:
                                    if data not in gambitColumns:
                                        gambitColumns.append(data)
                                else:
                                    if data not in medalsColumns:
                                        medalsColumns.append(data)
                            for c in sorted(gambitColumns):
                                try:
                                    if c in pvpstrings:
                                        insertData.update( {c: str(carnageData['values'][c]['basic']['displayValue'])} )
                                    else:
                                        insertData.update( {c: float(carnageData['values'][c]['basic']['value'])} )
                                except:
                                    insertData.update( {c: 0} )
#                            print(insertData)
                            statsData = gambitPVP(**insertData)
                            statsData.save()
                    except:
                        print(f'Get Carnage Error for Player:{getGuardianName(membershipId)} Guardian:{characterId} Activity:{activityId}')
                        raise
#                            continue
        print(f'{gamefound:3} matches found. {gameexist:3} matches already exist. {gameadded:3} matches added for Player: {getGuardianName(membershipId)} > {characterId}')
