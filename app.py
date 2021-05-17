from flask import Flask, render_template, abort, request
import os, requests, json

app = Flask(__name__)
URL_BASE="https://app.ticketmaster.com/discovery/v2/"
key=os.environ["key"]
with open("./codpaises.json") as fichero:
	codpaises=json.load(fichero)

@app.route('/',methods=["GET","POST"])
def buscador():
	if request.method=="GET":
		return render_template("buscador.html")
	else:
		cod=request.form.get("codigo")
		tip=request.form.get("tipo")
		filtro=request.form.get("filtro")
		payload={'apikey':key,'size':20}
		tipos=["Deporte","Música","Arte y teatro","Cine","Variado","Indefinido"]
		return render_template("buscador.html",filtro=filtro,codpaises=codpaises,tipos=tipos,cod=cod,tip=tip)

@app.route('/ultimos')
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


port=os.environ["PORT"]
app.run('0.0.0.0',int(port),debug=True)