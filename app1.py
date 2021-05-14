#Este programa saca los últimos eventos programados en España, junto con la fecha
#y la ciudad en la que se celebra el evento.
import requests
import os
URL_BASE="https://app.ticketmaster.com/discovery/v2/"
key=os.environ["key"]
payload={'apikey':key,'countryCode':'ES','size':50,'sort':'date,desc'}
r=requests.get(URL_BASE+'events.json',params=payload)
if r.status_code == 200:
	doc=r.json()
	for e in doc.get("_embedded").get("events"):
		print(f"Evento: {e.get('name')}")
		print(f"Fecha: {e.get('dates').get('start').get('localDate')}")
		print(f"Ciudad: {e.get('_embedded').get('venues')[0].get('city').get('name')}")
		print(f"ID: {e.get('id')}")
		print()