# Derelict

A collection of scripts used to browse the Bugnie API


The repo for the API can be found here: https://github.com/Bungie-net/api

You can also use the above link to get the link to apply for an API key


Full Documentation: https://bungie-net.github.io/multi/index.html

---
## Storing your api key outside of the project:

#### Create a folder under /home/user/.local/lib/python3.6/site-packages/

*mkdir /home/user/.local/lib/python3.6/site-packages/apikeys*

#### Create a file to store you key(s):

*touch /home/user/.local/lib/python3.6/site-packages/apikeys/bungie.py*

*APIKEY = "X-API-Key":'123456789teneleventwelve'*

#### Call your package within your file:

*from apikeys import bungie*
*HEADERS = bungie.APIKEY*
