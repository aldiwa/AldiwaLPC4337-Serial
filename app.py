#!/usr/bin/env python
# coding: utf-8
# Programa : Aldiwa Serial
# Autor : Maicon Gabriel Schmitz
# Site : http://www.aldiwa.com.br

# Carrega as bibliotecas
import time, sys, threading, datetime
import serial
import requests
import logging
import pprint
import re
from ConfigParser import SafeConfigParser

# Carrega as configuracoes
config = SafeConfigParser()
config.read('.env')

# Arquivo de log
arquivo_log = config.get('arquivo_log', 'arquivo')
logging.basicConfig(level=logging.DEBUG, filename=arquivo_log)

url_log = config.get('api_local', 'url_log')
url_api = config.get('api_local', 'url_api')

# Funcionalidade de log
def logar(sensor, mensagem):
    retorno = requests.post(url=url_log.format(sensor, mensagem))
    print retorno

# Funcionalidade de Chamada da API
def chamadaAPI(urlchamada, secao, sensor, conteudo):
    # Grava os dados de temperatura
    try:
        retorno = requests.post(url=urlchamada.format(secao, sensor, conteudo))
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        raise Exception("Erro: Tempo excedido")
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        raise Exception("Erro: Muitos redirecionamentos")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise Exception("Erro: Catastrofico")
        print e
        sys.exit(1)

# Configura a conexão com porta serial
conexaoSerial = serial.Serial()
conexaoSerial.port = '/dev/tty.usbserial'
conexaoSerial.baudrate = 115200
conexaoSerial.timeout = 1

# Conecta na porta serial
conexaoSerial.open()
conexaoSerial.isOpen()

while 1:
    try:
        # Captura os dados enviados pelo dispositivo
        dados = conexaoSerial.readline()

        # Remove as quebras de linha
        dados = dados.rstrip('\r\n')

        # Se a string possui os delimitadores
        if dados.startswith('#') and dados.endswith('#'):
            # Remove os delimitadores da string
            dados = re.sub('[#]', '', dados)

            # Obtem os dados
            tipo = dados.split(";")[0]
            sensor = dados.split(";")[1]
            dataatual = dados.split(";")[2]
            valor = dados.split(";")[3]
        
            # Testa o tipo dos valores    
            if tipo == "0":
                print 'uptime'
            elif tipo == "1":
                if sensor == "1":
                    # Grava os dados de fluxo de agua
                    chamadaAPI(url_api, 'fluxoagua', sensor, valor)
                    print 'fluxo'
                    print valor
                    print dataatual
                else:
                    # Grava os dados de vazao de agua
                    chamadaAPI(url_api, 'vazaoagua', 1, valor)
                    print 'possui vazao de agua'
                    print valor
                    print dataatual
            elif tipo == "2":
                # Grava os dados de temperatura
                chamadaAPI(url_api, 'temperatura', sensor, valor)
            elif tipo == "3":
                # Grava os dados de umidade
                chamadaAPI(url_api, 'umidade', sensor, valor)
            else:
                print 'tipo nao implementado'
            

            # Percorre os valores da string
            

    except KeyboardInterrupt:
        print "\nFechando..."
        conexaoSerial.close()
