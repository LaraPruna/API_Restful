import requests
import os
URL_BASE="https://app.ticketmaster.com/discovery/v2/"
key=os.environ["key"]
payload={'apikey':key,'countryCode':'ES'}
r=requests.get(URL_BASE+'events.json',params=payload)
if r.status_code == 200:
	doc=r.json()
	for e in doc.get("_embedded").get("events"):
		print (e.get("name"))