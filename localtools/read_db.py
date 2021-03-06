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
    classes = []
    temp_classes = GuardianClass.objects.filter(guardianId=gid).values('guardianClassId')
    for c in temp_classes:
        classes.append(c['guardianClassId'])
    return classes

def getClanList():
    guardian_list = []
    for g in GuardianId.objects.filter(active=1).values('guardianId'):
        guardian_list.append(g['guardianId'])
    return guardian_list

def getGuardianNameByClass(cid):
    gid = []
    temp_gid = GuardianClass.objects.filter(guardianClassId=cid).values('guardianId')
    for g in temp_gid:
        gid.append(g['guardianId'])
    name = getGuardianName(gid[0])
    return name

def getGuardianClassByClassId(cid):
    temp = []
    temp_cid = GuardianClass.objects.filter(guardianClassId=cid).values('guardianClass')
    for c in temp_cid:
        temp.append(c['guardianClass'])
    return classType(temp[0])

def classType(classId):
    if classId == 0:
        classType = 'Titan'
    elif classId == 1:
        classType = 'Hunter'
    else:
        classType = 'Warlock'
    return classType

#print(getGuardianId(sys.argv[1]))

for guardian in getClanList():
#    name = getGuardianName(guardian)
    classes = getGuardianClasses(guardian)
#    print(f'{name} {classes}')
#    print(classes)
    for cid in classes:
        name = getGuardianNameByClass(int(cid))
        matchCount = gambitStats.objects.filter(guardianId=cid).aggregate(Max('motesLost'))
#        print(matchCount['motesLost__max'])
        if matchCount['motesLost__max'] != None:
            print(f'{name}\t{getGuardianClassByClassId(cid)}:\t{matchCount}')

#matchCount = gambitStats.objects.all().values('guardianId')
#print(matchCount)
