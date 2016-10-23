# AldiwaLPC4337-Serial
Interface de comunicação serial entre a LPCXpresso4337 e o computador (ou outros equipamentos)

#Configuração do ambiente

Criei um arquivo com o nome .env, ajustando-o com as configurações do seu ambiente:

[base_dados_local]
conexao = sqlite:///aldiwa.db

[arquivo_log]
arquivo = aldiwa-pi.log

[api_local]
url_log = http://127.0.0.1:4000/log/sensor/{}/mensagem/{}
url_api = http://127.0.0.1:4000/{}/sensor/{}/medicao/{}

[api_remota]
url_log = http://ENDERECO-DO-DOMINIO:4000/log/sensor/{}/mensagem/{}
url_api = http://ENDERECO-DO-DOMINIO:4000/{}/sensor/{}/medicao/{}

[servidor]
host = 0.0.0.0
porta = 4000

#Executando o projeto

O projeto é dividido em 2 programas principais.

O primeiro é o app.py, o responsável por receber os dados via serial e encaminhar para a API.

O segundo é a API, responsável por receber os dados e gerenciar o envio destes dados para a API online, ou então, por gravar localmente para posterior envio para a API online.