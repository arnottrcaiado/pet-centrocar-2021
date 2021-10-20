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

#
# endpoint para busca de nomes e localização do sexo
# https://ceontrocarPet;pythonanywhere.com/buscasexo?nome=PAULO
#
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
            nome, sexo = procNomes( nome )
            return json.dumps({"Nome" : nome, "Sexo": sexo })

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
                    nome, sexo = procNomes( nome )
                    return json.dumps({"Nome" : nome, "Sexo": sexo })
            else :
                return json.dumps({"Nome" : "**incompleto**", "Sexo": "**Inexistente**"})
        return json.dumps({"Erro" : "**autentic**" })

# -------------------------------------------------------------------------------------------
# funcao para percorrer o dataframe procurando os nomes alterativos
# chamada quando o nome principal, indexado, não é localizado
def procNomes( nome ) :
    for i in range(len(df)) :
      nam = df['names'][i].split(sep='|')
      for j in range(len(nam)):
        if nome == nam[j] :
            sex = df['classification'][i]
            return str(nam[j]), str(sex)
    return str(nome), "**Inexistente**"

