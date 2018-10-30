#!/usr/bin/env python3

import requests
import datetime
import json
import sys
import pprint
import django
django.setup()

from django.db import models
from django.db.models import Sum,Max
from gambitapp.models import gambitStats,GuardianId,GuardianClass,nightfallStrikes

import bungotools
from apikeys import bungie
HEADERS = bungie.APIKEY

gambitColumns = []
medalsColumns = []
match_list = []
temp_list = []
guardian_list = []
insertData = {}
pp = pprint.PrettyPrinter(indent=2)
bungie_url='https://www.bungie.net/Platform'

#Get all unique matchIds from db
def getMatchList():
    return bungotools.getdbListValues(gambitStats.objects.all().values('matchId'),'matchId')

def getGuardianName(gid):
    name = GuardianId.objects.filter(guardianId=gid).values('guardianName')
    return name[0]['guardianName']

def getGuardianId(name):
    gid = GuardianId.objects.filter(guardianName=name).values('guardianId')
    return gid[0]['guardianId']

def getGuardianClasses(gid):
    return bungotools.getdbListValues(GuardianClass.objects.filter(guardianId=gid).values('guardianClassId'),'guardianClassId')

def getClanList():  
    return bungotools.getdbListValues(GuardianId.objects.filter(active=1).values('guardianId'),'guardianId')

def getGuardianNameByClass(cid):
    gid = bungotools.getdbListValues(GuardianClass.objects.filter(guardianClassId=cid).values('guardianId'),'guardianId')
    name = getGuardianName(gid[0])
    return name

def getGuardianClassByClassId(cid):
    temp = bungotools.getdbListValues(GuardianClass.objects.filter(guardianClassId=cid).values('guardianClass'),'guardianClass')
    return bungotools.getClassType(temp[0])

def getClanGuardianList():
    classes = []
    for guardian in getClanList():
        for g in getGuardianClasses(guardian):
            classes.append(g)
    return classes

def buildLeaderBoard(stats,string):
    s = [(k, statsm[k]) for k in sorted(statsm, key=statsm.get, reverse=True)]
    print(f'{string}')
    for k,v in s[:5]:
        print(f'{getGuardianNameByClass(int(k)):20}: {v}')

def getLeaderBoard(statType, statMod):
   statType = 0 

def lookupActivityName(uid):
    hashIdentifier = uid
    entityType = 'DestinyActivityDefinition'
    stuff_url = bungie_url + f'/Destiny2/Manifest/{entityType}/{hashIdentifier}/'
    stuff = requests.get(stuff_url, headers=HEADERS)
    if 'selectionScreenDisplayProperties' in stuff.json()['Response']:
        details = stuff.json()['Response']['displayProperties']['name'] + ':' + stuff.json()['Response']['selectionScreenDisplayProperties']['description'].replace('\n',' ')
    else:
        details = stuff.json()['Response']['displayProperties']['name'] + ':' +  stuff.json()['Response']['displayProperties']['description']
    return details

print('\n')
orderednight = nightfallStrikes.objects.order_by('matchDate').reverse().values('matchId').distinct()
#print(orderednight[:5])

standing = 1
header='{:4}|{:8}|{:25}|{:10}|{:51}|'.format('No.',' Score',' Nightfall','Date',' Guardians')
print(header)
for night in orderednight[:10]:
    guards = []
    nid = night['matchId']
    score = nightfallStrikes.objects.filter(matchId=nid).values('teamScore')[0]['teamScore']
    nguardians = nightfallStrikes.objects.filter(matchId=nid).values('guardianId')
    strike = nightfallStrikes.objects.filter(matchId=nid).values('strikeId')[0]['strikeId']
    date = nightfallStrikes.objects.filter(matchId=nid).values('matchDate')[0]['matchDate']
    for guardian in nguardians:
        guards.append(getGuardianNameByClass(guardian['guardianId']))
    name = lookupActivityName(strike).split(':')[1]
    print(f"{standing:4}|{score:8}|{name:25}|{date}| {'  '.join(guards):50}|")
    standing += 1


















#            print(f'{name}\t{getGuardianClassByClassId(cid)}:\t{matchCount}')
#    if statAgg:
#print(sorted(statAgg.values()))
#stuff = sorted(statAgg.values(), key=lambda x: int(x[1]), reverse=True)
#print(stuff)
#for key in sorted(statAgg.values(),reverse=True):
#    print(f'{getGuardianNameByClass(key)} : {statAgg[key]}')


