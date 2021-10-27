#
# FACULDADE SENAC
# Extensão Tecnológica
# Projeto PET CENTROCAR
# Orientador - Prof. Arnott Ramos Caiado
#

from flask import Flask, json, request, render_template
import pandas as pd
import sys
sys.path.insert(0,'/home/centrocarPet')
import pet_headers as keys                  # chaves da api e segurança

import matplotlib.pyplot as plt # biblioteca para estatisticas e graficos
import io
import base64


arquivo = '/home/centrocarPet/mysite/dados/grupos.csv'  # arquivo com nomes

df = pd.read_csv( arquivo )


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'PET-Centrocar. Use https://centrocarPet.pythonanywhere.com/buscasexo?nome=PAULO'

#
# endpoint para busca de nomes e localização do sexo
# https://centrocarPet.pythonanywhere.com/buscasexo?nome=PAULO
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
                return json.dumps({"Nome" : "**incompleto**", "Sexo": "*NotSearch**"})
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
    return str(nome), "*NotFound*"


# --------------------------------------------------------------------------------------------
# sequencia exemlo para gerar um grafico temporario e retorna url para um template
@app.route('/grafico', methods=['GET'] )
def exgraph() :

    equipes = ['A','B','C']
    vendas = [100,20,200]
    nomes = ['Equipes','Valores']
    df = pd.DataFrame( list(zip(equipes,vendas)), columns=nomes, index = equipes)

    img = io.BytesIO()
    df.plot( kind = 'barh', color='r')
    plt.title(' TITULO - Exemplo 1' )
    plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    grafico1= build_graph( graph_url )

    img = io.BytesIO()
    df.plot( kind = 'bar', color='g')
    plt.title(' TITULO - Exemplo 2 ' )
    plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    grafico2= build_graph( graph_url )

    img = io.BytesIO()
    df.plot.pie( y='Valores')
    plt.title(' TITULO - Exemplo 3 ' )
    plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    grafico3= build_graph( graph_url )

    return render_template( 'graficos.html', grafico1=grafico1, grafico2 = grafico2, grafico3=grafico3 )

# funcao para dar o tratamento final para o grafico gerado - para retornar url
def build_graph(graph_url):
    return 'data:image/png;base64,{}'.format(graph_url)