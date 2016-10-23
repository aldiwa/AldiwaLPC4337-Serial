from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from basedados import VazaoAgua, FluxoAgua, Temperatura, Umidade, Log, Base
import datetime
import requests
import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore',
 r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
 "and SQLAlchemy must convert from floating point - rounding errors and other "
 "issues may occur\. Please consider storing Decimal numbers as strings or "
 "integers on this platform for lossless storage\.$",
 SAWarning, r'^sqlalchemy\.sql\.type_api$')
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('.env')
conexao_local = config.get('base_dados_local', 'conexao')

engine = create_engine(conexao_local)
Base.metadata.bind = engine 
DBSession = sessionmaker(bind=engine)
session = DBSession()

global url_log
global url_api

url_log = config.get('api_remota', 'url_log')
url_api = config.get('api_remota', 'url_api')

app = Flask(__name__)

@app.route("/")
def main():
    temperatura = session.query(Temperatura).order_by(Temperatura.id.desc()).first()
    if temperatura is None:
        temperatura = 0
    else:
        temperatura = temperatura.medicao

    umidade = session.query(Umidade).order_by(Umidade.id.desc()).first()
    if umidade is None:
        umidade = 0
    else:
        umidade = umidade.medicao
    
    fluxoagua = session.query(FluxoAgua).order_by(FluxoAgua.id.desc()).first()
    if fluxoagua is None:
        fluxoagua = 0
    else:
        fluxoagua = fluxoagua.medicao
    
    return render_template('index.html', title='Aldiwa', temperatura=format(temperatura, '.2f'), umidade=format(umidade, '.2f'), fluxoagua=format(fluxoagua, '.2f'))

@app.route('/log/sensor/<sensor>/mensagem/<mensagem>', methods=['POST'])
def api_logar(sensor, mensagem):
    # Chama a API remota para gravar os dados de log
    try:
        retorno = requests.post(url=url_log.format(sensor, mensagem))
    except:
        # Grava os dados de log localmente
    	registro = Log(sensor_id=sensor, mensagem=mensagem, datahora=datetime.datetime.now())
    	session.add(registro)
    	session.commit()
    	return jsonify(retorno=1)

@app.route('/vazaoagua/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_vazaoagua(sensor, medicao):
    # Chama a API remota para gravar os dados de vazao de agua
    try:
        retorno = requests.post(url=url_api.format('vazaoagua', sensor, medicao))
    except:
        # Grava os dados de vazao de agua localmente
       registro = VazaoAgua(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
       session.add(registro)
       session.commit()
       return jsonify(retorno=1)

@app.route('/fluxoagua/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_fluxoagua(sensor, medicao):
    # Chama a API remota para gravar os dados de fluxo de agua
    try:
        retorno = requests.post(url=url_api.format('fluxoagua', sensor, medicao))
    except:
        # Grava os dados de fluxo de agua localmente
	   registro = FluxoAgua(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
	   session.add(registro)
	   session.commit()
	   return jsonify(retorno=1)

@app.route('/temperatura/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_temperatura(sensor, medicao):
    # Chama a API remota para gravar os dados de temperatura
    try:
        retorno = requests.post(url=url_api.format('temperatura', sensor, medicao))
    except:
        # Grava os dados de temperatura localmente
        registro = Temperatura(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
        session.add(registro)
        session.commit()
        return jsonify(retorno=1)

@app.route('/umidade/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_umidade(sensor, medicao):
    # Chama a API remota para gravar os dados de umidade
    try:
        retorno = requests.post(url=url_api.format('umidade', sensor, medicao))
    except:
        # Grava os dados de umidade localmente
        registro = Umidade(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
        session.add(registro)
        session.commit()
        return jsonify(retorno=1)

@app.route('/aldiwa', methods=['GET'])
def api_aldiwa():
    return jsonify(aldiwa='aldiwa',
                   versao='0.1')

if __name__ == "__main__":
    app.run(host=config.get('servidor', 'host'), port=config.get('servidor', 'porta'))
    #from gevent.wsgi import WSGIServer
    #http_server = WSGIServer(('0.0.0.0', 4000), app)
    #http_server.serve_forever()