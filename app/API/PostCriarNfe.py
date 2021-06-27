import requests
from pprint import pprint

_print = print
#print = pprint

url = 'http://host.docker.internal:8080/nfe'

user_data = {
    "motoristaDTO" : {
        "cpf" : "111.222.333/44",
        "nome" : "BRUNO BARBOSA Mendonca"
    },
    "codPlantaDTO" : {
        "descricaoOrigem" : "Destino_SP",
        "cidadeOrigem" : "Osasco",
        "estadoOrigem" : "São Paulo"
    },
    "codSlipDTO" : {
        "data" : "05/07/2000"
    },
    "codRegistroDTO" : {
        "data" : "05/07/2000"
    },
    "transportadoraDTO" : {
        "nome" : "Brunin Transportes"
    },
    "numNfe" : "78943213",
    "numSerie" : "5555555",
    "docTransporte" : 666666,
    "placa" : "A7HB879",
    "perfilCarga" : "ensacada",
    "estado" : 0
}

response = requests.post(url=url, json=user_data)

if response.status_code >= 200 and response.status_code <= 299:
    #Sucesso
    print('Status Code',response.status_code)
    print('Reason',response.reason)
    print('Texto',response.text)
    #print('JSON',response.json())
    #print('Bytes',response.content)
else:
    #erros
    print('Status Code',response.status_code)
    print('Reason',response.reason)
    print('Texto',response.text)