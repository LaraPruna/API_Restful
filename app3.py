#Este programa permite ver los detalles de un evento, una atracción (artista, grupo, equipo, etc.)
#o un lugar en el que se realizan eventos. Primero, se pedirá al usuario el nombre de uno de estos
#a modo de filtro, y se mostrará por pantalla una lista de eventos, atracciones o lugares que se correspondan
#con ese nombre junto con su ID. Para ver los detalles, el usuario deberá introducir esa ID.
import requests
import os
URL_BASE="https://app.ticketmaster.com/discovery/v2/"
key=os.environ["key"]
payload={'apikey':key,'size':50}
opcion=int(input('''Selecciona un tipo de búsqueda:
1. Eventos
2. Atracción (Artista, grupo, equipo...)
3. Lugar de eventos

Opción: '''))
while opcion < 1 or opcion > 3:
	print("Opción incorrecta.")
	opcion=int(input('''Selecciona un tipo de búsqueda:
1. Eventos
2. Atracción (Artista, grupo, equipo...)
3. Lugar de eventos

Opción: '''))

if opcion == 1:
	nombre=input("Introduce el nombre de un evento: ")
	payload['keyword']=nombre
	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay eventos con ese nombre registrados en la base de datos.")
		else:
			for e in doc.get("_embedded").get("events"):
				print(f"Evento: {e.get('name')}")
				print(f"Fecha: {e.get('dates').get('start').get('localDate')}")
				print(f"Tipo de evento: {e.get('_embedded').get('attractions')[0].get('classifications')[0].get('segment').get('name')}")
				print(f"ID: {e.get('id')}")
				print()
			ID=input("Introduce la ID del evento que quieras ver: ")
			del payload['keyword']
			r2=requests.get(URL_BASE+'events/'+ID,params=payload)
			evento=r2.json()
			print(f"Evento: {evento.get('name')}")
			print(f"Fecha: {evento.get('dates').get('start').get('localDate')}")
			print(f"Ciudad: {evento.get('_embedded').get('venues')[0].get('city').get('name')}")
			print(f"Lugar del evento: {evento.get('_embedded').get('venues')[0].get('name')}")
			print(f"Tipo de evento: {evento.get('_embedded').get('attractions')[0].get('classifications')[0].get('segment').get('name')}")
			if evento.get('priceRanges') != None:
				print(f"Moneda: {evento.get('priceRanges')[0].get('currency')}")
				print("Rango de precios:")
				print(f"Mínimo: {evento.get('priceRanges')[0].get('min')}")
				print(f"Máximo: {evento.get('priceRanges')[0].get('max')}")
			print(f"Comprar ticket: {evento.get('url')}")

elif opcion == 2:
	nombre=input("Introduce el nombre de un artista, grupo, equipo, etc.: ")
	payload['keyword']=nombre
	r=requests.get(URL_BASE+'attractions.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay atracciones con ese nombre registrados en la base de datos.")
		else:
			for a in doc.get("_embedded").get("attractions"):
				print(f"Atracción: {a.get('name')}")
				print(f"Tipo de atracción: {a.get('classifications')[0].get('segment').get('name')}")
				print(f"ID: {a.get('id')}")
				print()
			ID=input("Introduce la ID de la atracción que quieras ver: ")
			del payload['keyword']
			r2=requests.get(URL_BASE+'attractions/'+ID,params=payload)
			atraccion=r2.json()
			print(f"Atracción: {atraccion.get('name')}")
			print(f"Tipo de atracción: {atraccion.get('classifications')[0].get('segment').get('name')}")
			print(f"Género: {atraccion.get('classifications')[0].get('genre').get('name')}")
			if atraccion.get('externalLinks') != None:	
				print(f"Redes sociales y sitios web:")
				for sitio in atraccion.get('externalLinks'):
					print(sitio.upper())
					for enlace in atraccion.get('externalLinks').get(sitio):
						print(enlace.get('url'))
			print(f"Número de eventos registrados en la base de datos: {atraccion.get('upcomingEvents').get('ticketmaster')}")
			print(f"Eventos programados: {atraccion.get('url')}")

elif opcion == 3:
	nombre=input("Introduce un lugar de eventos: ")
	payload['keyword']=nombre
	r=requests.get(URL_BASE+'venues.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		if doc.get("_embedded")==None:
			print("De momento no hay lugares con ese nombre registrados en la base de datos.")
		else:
			for l in doc.get("_embedded").get("venues"):
				print(f"Lugar: {l.get('name')}")
				print(f"Ciudad: {l.get('city').get('name')}")
				print(f"ID: {l.get('id')}")
				print()
			ID=input("Introduce la ID del lugar que quieras ver: ")
			del payload['keyword']
			r2=requests.get(URL_BASE+'venues/'+ID,params=payload)
			lugar=r2.json()
			print(f"Lugar: {lugar.get('name')}")
			print(f"Ciudad: {lugar.get('city').get('name')}")
			print(f"País: {lugar.get('country').get('name')}")
			print(f"Dirección: {lugar.get('address').get('line1')}")
			print(f"Número de eventos programados: {lugar.get('upcomingEvents').get('_total')}")
			print(f"Eventos programados: {lugar.get('url')}")