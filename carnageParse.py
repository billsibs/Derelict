#!/usr/bin/env python3

import json
import sys
import pprint
gambitColumns = []
medalsColumns = []
pp = pprint.PrettyPrinter(indent=2)

with open('carnageRaw.json') as json_file:
    json_data = json.load(json_file)

#print(json_data)

for block in json_data['Response']['entries']:
#    print(block['characterId'])
    characterId = block['characterId']
#    print(block['extended']['values'])
    for data in block['extended']['values']:
        if 'medal' not in data:
            if data not in gambitColumns:
                gambitColumns.append(data)
        else:
            if data not in medalsColumns:
                medalsColumns.append(data)
    for c in sorted(gambitColumns):
        try:
            print(characterId + '>' + c + ':' + block['extended']['values'][c]['basic']['displayValue'])
        except:
            print(characterId + '>' + c + ':' + 'NULL')
#    for c in medalsColumns:
#        try:
#            print(characterId + '>' + c + ':' + block['extended']['values'][c]['basic']['displayValue'])
#        except:
#            print(characterId + '>' + c + ':' + 'NULL')
#print(columns)
