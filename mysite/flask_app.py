#
# FACULDADE SENAC
# Extensão Tecnológica
# Projeto PET CENTROCAR
# Orientador - Prof. Arnott Ramos Caiado
#

from flask import Flask, json, request
import pandas as pd

import sys
sys.path.insert(0,'/home/centrocarPet')
import pet_headers as keys                  # chaves da api e segurança

arquivo = '/home/centrocarPet/mysite/dados/grupos.csv'  # arquivo com nomes

df = pd.read_csv( arquivo )


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Mensagem aqui'

@app.route('/buscasexo', methods=['GET'] )
def procNome( ):
    nome = request.args.get('nome') # obtem parametro da url . ?nome=JOSE
    if nome != None :
        nome = nome.upper()
        busca = df.loc[df['name']== nome]
        if len(busca) > 0 :
            nomeEncontrado = busca['name'].to_list()
            sexEncontrado = busca['classification'].to_list()
            return json.dumps({"Nome": nomeEncontrado[0], "Sexo" : sexEncontrado[0] })
        else:
            return json.dumps({"Nome" : nome, "Sexo": "**Inexistente**"})
    else : # não foi encontrado parâmetro na linha url - verificar header e parametros
        chave = request.headers.get('secret-key')
        if chave == keys.key_header_nome : # chave de autenticação para a API
            nome = request.form.get('nome')
            if nome != None :
                nome = nome.upper()
                busca = df.loc[df['name']== nome]
                if len(busca) > 0 :
                    nomeEncontrado = busca['name'].to_list()
                    sexEncontrado = busca['classification'].to_list()
                    return json.dumps({"Nome": nomeEncontrado[0], "Sexo" : sexEncontrado[0] })
                else:
                    return json.dumps({"Nome" : nome, "Sexo": "**Inexistente**"})
            else :
                return json.dumps({"Nome" : "**incompleto**", "Sexo": "**Inexistente**"})
        return json.dumps({"Erro" : "**autentic**" })

