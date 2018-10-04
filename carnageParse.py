#!/usr/bin/env python3

import json
import sys
import pprint
gambitColumns = []
medalsColumns = []
pp = pprint.PrettyPrinter(indent=2)

#Open local carnage file instead of constant calls to API. 
#This is for local testing
with open('carnageRaw.json') as json_file:
    json_data = json.load(json_file)

for block in json_data['Response']['entries']:
    characterId = block['characterId']
    for data in block['extended']['values']:
        #Only collect gambitStats here. Save medal collection for later
        if 'medal' not in data:
            if data not in gambitColumns:
                gambitColumns.append(data)
        #Medal collection. Medals can differ per game. 
        #They are not constant variables like gambit stats
        else:
            if data not in medalsColumns:
                medalsColumns.append(data)
    #Print out gambit stats
    for c in sorted(gambitColumns):
        try:
            print(characterId + '>' + c + ':' + block['extended']['values'][c]['basic']['displayValue'])
        except:
            print(characterId + '>' + c + ':' + 'NULL')
#Print out for medals. This is not necessary at this time
#    for c in medalsColumns:
#        try:
#            print(characterId + '>' + c + ':' + block['extended']['values'][c]['basic']['displayValue'])
#        except:
#            print(characterId + '>' + c + ':' + 'NULL')
#print(columns)
