# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from os import pardir

from flask.wrappers import Response
from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import requests

@blueprint.route('/index', methods=['POST','GET'])
def index():
    url = 'http://host.docker.internal:8080/nfe'
    if request.method == 'POST':
        mensagem = ""
        user_data = {
            "motoristaDTO" : {
                "cpf" : request.form['cpf'],
                "nome" : request.form["nomeMotorista"]
            },
            "codPlantaDTO" : {
                "descricaoOrigem" : request.form["descricao"],
                "cidadeOrigem" : request.form["cidade"],
                "estadoOrigem" : request.form["estadoOrigem"]
            },
            "codSlipDTO" : {
                "data" : request.form["dataSlip"]
            },
            "codRegistroDTO" : {
                "data" : request.form["dataSlip"]
            },
            "transportadoraDTO" : {
                "nome" : request.form["nomeTransportadora"]
            },
            "numNfe" : request.form["numNfe"],
            "numSerie" : request.form["numSerie"],
            "docTransporte" : request.form["docTransporte"],
            "placa" : request.form["placa"],
            "perfilCarga" : request.form["perfilCarga"],
            "estado" : request.form["statusNota"]
        }        
        response = requests.post(url=url, json=user_data)
        if response.status_code >= 200 and response.status_code <= 299:
            mensagem = "Nota fiscal salva" 
        if response.status_code > 400:
            mensagem = "Não foi possivel salvar a Nota fiscal"
        response = requests.get(url=url)
        return render_template('index.html', segment='index.html', title="teste", mensagem=mensagem, response=response)
    
    response = requests.get(url=url)

    return render_template('index.html', segment='index.html', title="teste", response=response.json())

@blueprint.route('/tables-data', methods=['POST','GET'])
def tables():
    url = 'http://host.docker.internal:8080/nfe'
    mensagem = ""

    if request.method == 'POST':
        if request.form.get('estadoNF'):
            url_put = url + "/" + request.form["numNfe"]
            user_data= {
                "estado" : request.form["estadoNF"]
            }
            response = requests.put(url=url_put,json=user_data)

            if response.status_code >= 200 and response.status_code <= 299:
                mensagem = "Nota fiscal editada com sucesso" 
            if response.status_code > 400:
                mensagem = "Falha ao editar a Nota fiscal"
        else:                        
            urlDel = url + "/" + request.form["numNfe"]
            response = requests.delete(urlDel)

            if response.status_code >= 200 and response.status_code <= 299:
                mensagem = "Nota fiscal excluida" 
            if response.status_code > 400:
                mensagem = "Falha ao excluir a Nota fiscal"

    responseGet = requests.get(url)
    return render_template('tables-data.html', segment='tables-data.html', title="title", mensagem=mensagem, response=responseGet.json())

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
