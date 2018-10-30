#!/usr/bin/env python3

import requests
import datetime
import json
import sys
import pprint
import django
django.setup()

from django.db import models

from gambitapp.models import GuardianId,nightfallStrikes

from apikeys import bungie
HEADERS = bungie.APIKEY

import bungotools

#Modes - PvP:5, PvE:7, Nightfall:16, Strikes:18, IronBanner:19, ScoredNightfall:46
#   Scored HeroicNightfall:47, Gambit:63, CompetitivePvE: 64
mode = 46

strikeColumns = []
temp_list = []
guardian_list = []
pp = pprint.PrettyPrinter(indent=2)

countLimit=200
groupType='1'
groupId='1669746'
membershipType='1'
bungie_url='https://www.bungie.net/Platform'



guardian_list = bungotools.getdbListValues(GuardianId.objects.filter(active=1).values('guardianId'), 'guardianId')

#Get all unique matchIds from db
def getStrikeList(tgid):
    temp_list = []
    for m in nightfallStrikes.objects.all().filter(guardianId=tgid).values('matchId'):
        temp_list.append(m['matchId'])
#    print(tgid)
#    print(len(sorted(set(temp_list))))
    return sorted(set(temp_list))
#print(match_list)
def getGuardianName(cid):
    name = GuardianId.objects.filter(guardianId=cid).values('guardianName')
    return name[0]['guardianName']

for clanMember in guardian_list:
    membershipId = str(clanMember)
    destinyMembershipId = membershipId
    profile_url = bungie_url + f'/Destiny2/{membershipType}/Profile/{membershipId}/?components=Characters'
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
#            print(profile.json()['Message'])
            sys.exit(0)
        continue
    #For each Guardian class, get their list of match IDs
    for characterId in cid:
        print(f'{len(getStrikeList(characterId))} matches found for {characterId}')
        gamefound=0
        gameadded=0
        gameexist=0
        activity_url = bungie_url + f'/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/?mode={mode}&count={countLimit}'
        try: #If error occurs, move on to next class 
            activity = requests.get(activity_url, headers=HEADERS)
        except:
            print(f'Activity lookup Error for Player:{getGuardianName(membershipId)} Guardian:{characterId}')
            continue
        #Check and see if gambit data exists, otherwise tell no gambit data found
        if activity.json()['Response']:
#            pp.pprint(activity.json())
            for instance in activity.json()['Response']['activities']:
#                pp.pprint(instance)
                gamefound += 1
#                print(characterId)
#                print(f'{len(getStrikeList(characterId))} matches found for {characterId}')
                if int(instance['activityDetails']['instanceId']) in getStrikeList(int(characterId)):
#                    print('Match Found. No need to add for ' + str(clanMember) )
                    gameexist += 1
                else:
                    gameadded += 1
#                    for strike in instance:
                    insertData = {}
#                            print(f'Debug: {characterId}')
                    #insertData.update( { 'guardianId': int(characterId) })
                    insertData.update( { 'matchId' : int(instance['activityDetails']['instanceId']) } )
                    insertData.update( { 'matchDate' : instance['period'] .split('T')[0] } )
                    insertData.update( { 'strikeId' : int(instance['activityDetails']['referenceId']) } )
                    insertData.update( { 'guardianId': int(characterId) })
                    for data in instance['values']:
                        if data not in strikeColumns:
                            strikeColumns.append(data)
                    for c in sorted(strikeColumns):
                        try:
                            insertData.update( {c: float(instance['values'][c]['basic']['value'])} )
                        except:
                            insertData.update( {c: 0} )
                    print(insertData)
#                    print(len(insertData))
                    statsData = nightfallStrikes(**insertData)
                    statsData.save()
        print(f'{gamefound:3} matches found. {gameexist:3} matches already exist. {gameadded:3} matches added for Player: {getGuardianName(membershipId)} > {characterId}')
