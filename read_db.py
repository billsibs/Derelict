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
from gambitapp.models import gambitStats,GuardianId,GuardianClass


gambitColumns = []
medalsColumns = []
match_list = []
temp_list = []
guardian_list = []
insertData = {}
pp = pprint.PrettyPrinter(indent=2)

#Get all unique matchIds from db
def getMatchList():
    for m in gambitStats.objects.all().values('matchId'):
        temp_list.append(m['matchId'])
    return sorted(set(temp_list))
#print(match_list)
def getGuardianName(gid):
    name = GuardianId.objects.filter(guardianId=gid).values('guardianName')
    return name[0]['guardianName']

def getGuardianId(name):
    gid = GuardianId.objects.filter(guardianName=name).values('guardianId')
    return gid[0]['guardianId']

def getGuardianClasses(gid):
    classes = {}
    temp_classes = GuardianClass.objects.filter(guardianId=gid).values('guardianClass','guardianClassId')
    for c in temp_classes:
        classes.update({c['guardianClass']: c['guardianClassId']})
    return classes
def getClanList():
    guardian_list = []
    for g in GuardianId.objects.filter(active=1).values('guardianId'):
        guardian_list.append(g['guardianId'])
    return guardian_list

def className(classId):
    if classId == 0:
        classType = 'Titan'
    elif classId == 1:
        classType = 'Hunter'
    else:
        classType = 'Warlock'
    return classType

#print(getGuardianId(sys.argv[1]))

for guardian in getClanList():
    name = getGuardianName(guardian)
    classes = getGuardianClasses(guardian)
#    print(classes)
    for c,cid in classes.items():
        matchCount = gambitStats.objects.filter(guardianId=cid).aggregate(Max('motesLost'))
#        print(matchCount['motesLost__max'])
        if matchCount['motesLost__max'] != None:
            print(f'{name}\t{className(c)}:\t{matchCount}')

#matchCount = gambitStats.objects.all().values('guardianId')
#print(matchCount)
