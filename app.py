from flask import Flask, render_template, abort, request
import os, requests, json

app = Flask(__name__)
URL_BASE="https://app.ticketmaster.com/discovery/v2/"
URL_BASE2="https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels/"
key=os.environ["key"]
key2=os.environ["key2"]
with open("./codpaises.json") as fichero:
	codpaises=json.load(fichero)
with open("./tipos.json") as fichero2:
	tipos=json.load(fichero2)

@app.route('/',methods=["GET","POST"])
def buscador():
	if request.method=="GET":
		return render_template("buscador.html")
	else:
		cod=request.form.get("codigo")
		tip=request.form.get("tipo")
		filtro=request.form.get("filtro")
		return render_template("buscador.html",filtro=filtro,codpaises=codpaises,tipos=tipos,cod=cod,tip=tip)

@app.route('/ultimos',methods=["GET","POST"])
def ultimos():
	payload={'apikey':key,'countryCode':'ES','size':10,'sort':'date,desc'}
	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		doc=r.json()
		cod=request.form.get("codigo")
		lista=[]
		for e in doc.get("_embedded").get("events"):
			dic={}
			dic['imagen']=e.get('images')[0].get('url')
			dic['evento']=e.get('name')
			dic['fecha']=e.get('dates').get('start').get('localDate')
			dic['ciudad']=e.get('_embedded').get('venues')[0].get('city').get('name')
			dic['id']=e.get('id')
			lista.append(dic)
		return render_template("ultimos.html",lista=lista)

@app.route('/listaeventos',methods=["POST"])
def lista_eventos():
	ciudad=request.form.get("ciudad")
	pais=request.form.get("codigo")
	clave=request.form.get("clave")
	tipo=request.form.get("tipo")
	fechainicio=request.form.get("fechainicio")

	if ciudad:
		payload={'apikey':key,'city':ciudad,'size':10,'sort':'date,desc'}

	elif pais:
		payload={'apikey':key,'countryCode':pais,'size':10,'sort':'date,desc'}

	elif clave:
		payload={'apikey':key,'keyword':clave,'size':10,'sort':'date,desc'}

	elif tipo:
		payload={'apikey':key,'classificationName':tipo,'size':10,'sort':'date,desc'}
	else:
		fechainicio=request.form.get("fechainicio")
		horainicio=request.form.get("horainicio")
		fechahorainicio=fechainicio+'T'+horainicio+':00Z'
		fechafin=request.form.get("fechafin")
		horafin=request.form.get("horafin")
		fechahorafin=fechafin+'T'+horafin+':00Z'
		payload={'apikey':key,'startDateTime':fechahorainicio,'endDateTime':fechahorafin,'size':10,'sort':'date,desc'}		

	r=requests.get(URL_BASE+'events.json',params=payload)
	if r.status_code == 200:
		lista=r.json()
		return render_template("listaeventos.html",lista=lista)
	else:
		abort(404)

@app.route("/detalles/<ident>", methods=["GET","POST"])
def detalles(ident):
	payload={'apikey':key,'size':10}
	payload2={'key':key2,'zoomLevel':16}
	r=requests.get(URL_BASE+'events/'+ident,params=payload)
	if r.status_code == 200:
		evento=r.json()
		pag='events'
		lon=evento.get('_embedded').get('venues')[0].get('location').get('longitude')
		lat=evento.get('_embedded').get('venues')[0].get('location').get('latitude')
		loc=requests.get(URL_BASE2+lat+','+lon,params=payload2)
		loc2=loc.url
		return render_template("detalles.html",evento=evento,pag=pag,loc=loc2)
	else:
		r=requests.get(URL_BASE+'attractions/'+ident,params=payload)
		if r.status_code == 200:
			atraccion=r.json()
			pag='attractions'
			return render_template("detalles.html",atraccion=atraccion,pag=pag)
		else:
			r=requests.get(URL_BASE+'venues/'+ident,params=payload)
			if r.status_code == 200:
				lugar=r.json()
				pag='venues'
				lon=lugar.get('location').get('longitude')
				lat=lugar.get('location').get('latitude')
				loc=requests.get(URL_BASE2+lat+','+lon,params=payload2)
				loc2=loc.url
				return render_template("detalles.html",lugar=lugar,pag=pag,loc=loc2)
			else:
				abort(404)


port=os.environ["PORT"]
app.run('0.0.0.0',int(port),debug=True)