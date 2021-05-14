#Este programa permite buscar eventos por diferentes filtros, que se muestran
#en un menú, y devuelve el nombre de 50 eventos junto con alguna otra información, como la
#fecha, la ciudad en la que se celebra o el tipo de evento.
import requests
import os
URL_BASE="https://app.ticketmaster.com/discovery/v2/"
key=os.environ["key"]
payload={'apikey':key,'size':50}
opcion=int(input('''Selecciona un filtro de búsqueda:
1. Ciudad
2. País
3. Tipo de evento
4. Clave
5. Intervalo de fechas

Opción: '''))
while opcion < 1 or opcion > 5:
	print("Opción incorrecta.")
	opcion=input('''Selecciona un filtro de búsqueda:
1. Ciudad
2. País
3. Tipo de evento
4. Clave
5. Intervalo de fechas

Opción: ''')
if opcion==1:
	ciudad=input("Introduce el nombre de la ciudad: ")
	payload['city']=ciudad
	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay eventos de esa ciudad registrados en la base de datos.")
		else:
			for e in doc.get("_embedded").get("events"):
				print(f"Evento: {e.get('name')}")
				print(f"Fecha: {e.get('dates').get('start').get('localDate')}")
				print(f"Tipo de evento: {e.get('_embedded').get('attractions')[0].get('classifications')[0].get('segment').get('name')}")
				print()

elif opcion==2:
	pais=input("Introduce el código del país (por ejemplo, ES para España): ")
	payload['countryCode']=pais
	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay eventos de ese país registrados en la base de datos.")
		else:
			for e in doc.get("_embedded").get("events"):
				print(f"Evento: {e.get('name')}")
				print(f"Fecha: {e.get('dates').get('start').get('localDate')}")
				print(f"Ciudad: {e.get('_embedded').get('venues')[0].get('city').get('name')}")
				print(f"Tipo de evento: {e.get('_embedded').get('attractions')[0].get('classifications')[0].get('segment').get('name')}")
				print()

elif opcion==3:
	opcion2=int(input('''Selecciona un tipo de evento de la siguiente lista:
1. Deporte
2. Música
3. Arte y teatro
4. Cine
5. Variado
6. Indefinido

Opción: '''))
	while opcion2 < 1 or opcion2 > 6:
		print("Opción incorrecta.")
		opcion2=int(input('''Selecciona un tipo de evento de la siguiente lista:
1. Deporte
2. Música
3. Arte y teatro
4. Cine
5. Variado
6. Indefinido

Opción: '''))
	if opcion2==1:
		payload['classificationName']="Sports"
	elif opcion2==2:
		payload['classificationName']="Music"
	elif opcion2==3:
		payload['classificationName']="Arts & Theatre"
	elif opcion2==4:
		payload['classificationName']="Film"
	elif opcion2==5:
		payload['classificationName']="Miscellaneous"
	else:
		payload['classificationName']="Undefined"
	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay eventos de ese tipo registrados en la base de datos.")
		else:
			for e in doc.get("_embedded").get("events"):
				print(f"Evento: {e.get('name')}")
				print(f"Fecha: {e.get('dates').get('start').get('localDate')}")
				print(f"Ciudad: {e.get('_embedded').get('venues')[0].get('city').get('name')}")
				print()
elif opcion==4:
	atraccion=input("Introduce una clave (artista, grupo, equipo, ciudad, etc.): ")
	payload['keyword']=atraccion
	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay eventos con esa clave registrados en la base de datos.")
		else:
			for e in doc.get("_embedded").get("events"):
				print(f"Evento: {e.get('name')}")
				print(f"Fecha: {e.get('dates').get('start').get('localDate')}")
				print(f"Ciudad: {e.get('_embedded').get('venues')[0].get('city').get('name')}")
				print(f"Tipo de evento: {e.get('_embedded').get('attractions')[0].get('classifications')[0].get('segment').get('name')}")
				print()
elif opcion==5:
	fechainicio=input("Introduce la fecha de inicio con formato YYYY-MM-DD: ")
	horainicio=input("Introduce una hora de inicio con formato HH-MI-SS: ")
	fechafin=input("Introduce la fecha de finalización con formato YYYY-MM-DD: ")
	horafin=input("Introduce una hora de finalización con formato HH-MI-SS: ")
	payload['startDateTime']=fechainicio+'T'+horainicio+'Z'
	payload['endDateTime']=fechafin+'T'+horafin+'Z'
	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay eventos con esa clave registrados en la base de datos.")
		else:
			for e in doc.get("_embedded").get("events"):
				print(f"Evento: {e.get('name')}")
				print(f"Ciudad: {e.get('_embedded').get('venues')[0].get('city').get('name')}")
				print(f"Tipo de evento: {e.get('_embedded').get('attractions')[0].get('classifications')[0].get('segment').get('name')}")
				print()