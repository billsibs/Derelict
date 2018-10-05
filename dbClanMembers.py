#!/usr/bin/env python3

import requests
import datetime

import django
django.setup()
from django.db import models
from gambitapp.models import GuardianId

from APIKEY import APIKEY
HEADERS = APIKEY

import pprint
pp = pprint.PrettyPrinter(indent=2)

guardians = GuardianId.objects.all().values()

print(guardians)

for g in guardians:
    print(g['guardianName'])

