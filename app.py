from flask import Flask, jsonify, request
from waitress import serve
import requests
import os

app = Flask(__name__)

#los comentarios son muy parecidos a app_directa.py, con alguna modificación

def obtener_incidencias_autopista(autopista):
    url = f"https://api.euskadi.eus/traffic/v1.0/incidences?_page=1"
    response = requests.get(url)
    data = response.json()
    incidencias = [incidencia for incidencia in data["incidences"] if incidencia["road"] == autopista.upper()]
    if incidencias:
        return incidencias[-1]
    else:
        resultado = {}
        resultado['mensaje'] = f"No se encontraron incidencias para la autopista {autopista}"
        resultado['valores validos'] = ['A-1', 'AP-1', 'A-8', 'AP-68', 'A-15']
        return resultado

def obtener_prediccion_tiempo(ciudad):
    cod = "null"

    if (ciudad.upper() == "BILBAO"):
        cod = "48020"
    elif (ciudad.upper() == "DONOSTIA"):
        cod = "20069"
    elif (ciudad.upper() == "VITORIA"):
        cod = "01059"
    with open(os.environ.get('APIKEY'), 'r') as f:
        api_key = f.readline()
        #cogemos el fichero donde se encuentra el apikey que se pasa por argumento como variable de entorno. Así podemos modificarla sin crear cada vez un contenedor y imagen nuevo.

    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{cod}"

    querystring = {"api_key":api_key}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    if "datos" in data:
        response = requests.request("GET", data["datos"], headers=headers, params=querystring)
        data = response.json()
        data = data[0]["prediccion"]["dia"][0]["temperatura"]
        resultado = {}
        resultado["mensaje"] = f"Prevision de temperatura en {ciudad.upper()}"
        resultado["temperatura minima"] = data["minima"]
        resultado["temperatura maxima"] = data["maxima"]
        return resultado

    else:
        resultado = {}
        resultado['mensaje'] = f"No se puede acceder al municipio {ciudad}"
        resultado['valores validos'] = ['Vitoria', 'Donostia', 'Bilbao']
        return resultado

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "OK"})

@app.route('/trafico/<autopista>', methods=['GET'])
def trafico(autopista):
    return jsonify(obtener_incidencias_autopista(autopista))

@app.route('/tiempo/<ciudad>', methods=['GET'])
def tiempo(ciudad):
    return jsonify(obtener_prediccion_tiempo(ciudad))

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
    #host = 0.0.0.0 significa que el servidor escuchará en todas las interfaces de red disponibles en el sistema
    #port = 5000 significa que el puerto que recibe las solicitudes es ese