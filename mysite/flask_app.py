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

# endpoint para busca de nomes e localização do sexo
# https://centrocarPet.pythonanywhere.com/buscasexo?nome=PAULO
#
@app.route('/buscasexo', methods=['GET'] )
def procNome( ):
    nome = request.args.get('nome') # obtem parametro da url . ?nome=JOSE
    if nome != None :
        lnome = nome.split()
        nome = lnome[0]
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
                lnome = nome.split()
                nome = lnome[0]
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


#-------------------------------------------------------------------------------------------------------------------------------------
# API para gerar um grafico x y
@app.route('/grafxy', methods=['GET','POST'])
def grafxy ():
    recebido = request.json
    if  request.form.get('x') != None and  request.form.get('y') != None  and request.form.get('nomes') != None or recebido != None :
        if recebido == None : # caso os parametros sejam recebidos diferentes de formato json
            x = request.form.get('x').split(sep=',')    # obtem valores para label eixo x
            y = request.form.get('y').split(sep=',')    # obtem valores para eyxo y - converter para numero
            nomes = request.form.get('nomes').split(sep=',')    # obtem valores para nomes das colunas
            y = list(map(lambda x : float(x), y))   # o mesmo que o anterior , na forma de funcao lambda - transforma os valores em float
            '''
            for i in range(len(y)) :    # transforma os valores para numeros
                y[i] = float(y[i])
            '''
        else : # caso seja recebido no formato json
            x = recebido['x']
            y = recebido['y']
            nomes = recebido['nomes']

        df = pd.DataFrame( list(zip(x,y)), columns=nomes, index = x)    # monta o dataframe
        img = io.BytesIO()
        df.plot( kind = 'bar', color='g')
        plt.title(' TITULO - Exemplo x y ' )
        plt.show()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        grafico= build_graph( graph_url )

        return render_template( 'graficoXY.html', grafico1=grafico )   # mostra a tela com grafico
    else :
        return json.dumps({ "ERRO": "Faltam Parâmetros X, Y" } )

# -----------------------------------------------------------------------------------------------------------
# API para gerar um grafico x y com chart.js - biblioteca bastante poderosa para graficos
# Use https://centrocarPet.pythonanywhere.com/grafxyJs
@app.route('/grafxyJs', methods=['GET','POST'])
def grafxyJs ():
    recebido = request.json
    if  request.form.get('x') != None and  request.form.get('y') != None  and request.form.get('nomes') != None or recebido != None :
        if recebido == None : # caso os parametros sejam recebidos diferentes de formato json
            x = request.form.get('x').split(sep=',')    # obtem valores para label eixo x
            y = request.form.get('y').split(sep=',')    # obtem valores para eyxo y - converter para numero
            nomes = request.form.get('nomes').split(sep=',')    # obtem valores para nomes das colunas
            y = list(map(lambda x : float(x), y))   # o mesmo que o anterior , na forma de funcao lambda - transforma os valores em float
            '''
            for i in range(len(y)) :    # transforma os valores para numeros
                y[i] = float(y[i])
            '''
        else : # caso seja recebido no formato json
            x = recebido['x']
            y = recebido['y']
            nomes = recebido['nomes']

        return render_template( 'graficoXY_JS.html', labels=x, values=y )   # mostra a tela com grafico
    else :
        return json.dumps({ "ERRO": "Faltam Parâmetros X, Y" } )

# ------------------------------------------------------------------
# exemplo de grafico com uso do chart.js
# Use https://centrocarPet.pythonanywhere.com/gjs
@app.route('/gjs')
def graf():
    params = {
        "x":["A","B","C","D","E","F","G"],
        "y":[100,120,100,50,80,90,120],
        "nomes":["Eq","Valores"]
    }
    params2 = {
        "x":["Blue","Red","Cian","Black","Pink","White","Green"],
        "y":[60,100,40,80,90,70,10],
        "nomes":["Times","Notas"]
    }

    x = params['x']
    y = params['y']
    x2=params2['x']
    y2=params2['y']

    # return render_template( 'graficoXY_JS.html', labels=x, values=y )   # mostra a tela com grafico
    return render_template( 'graficoXY_JS2.html', labels=x, values=y, labels2=x2, values2=y2 )   # mostra a tela com grafico

#


# função para dar o tratamento final para o grafico gerado - para retornar url
def build_graph(graph_url):
    return 'data:image/png;base64,{}'.format(graph_url)