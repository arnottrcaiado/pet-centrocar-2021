# pet-centrocar-2021
Projeto PET - FACEPE - Centrocar
Inicio: set/2021 - capacitações
        out/2021 - projeto de extensão
Coordenação: Prof. Arnott Ramos Caiado

Testes criados para apoio ao projeto - pythonanywhere.com

https://www.pythonanywhere.com/user/centrocarPet/


# rota para gerar grafico de barras
# na forma de API
#
http://centrocarpet.pythonanywhere.com/grafxy

parametros
x labels para os dados, separados por virgula
y valores numericos, separados por virgula
nomes nomes das colunas

Ex
![image](https://user-images.githubusercontent.com/69168575/139855040-8619f684-8498-4994-8ec1-78be289ac5a6.png)

Ex postman

![image](https://user-images.githubusercontent.com/69168575/139855288-26f75e84-31c4-4df6-9d51-b7a505c20546.png)

# ou formato json
parametros
x labels para os dados
y valores numericos
nomes nomes das colunas

{
    "x": ["1","2","3","4"],
    "y": [100,200,300,400],
    "nomes" : ["Eq","Valores"]
}

Ex postman formato json

![image](https://user-images.githubusercontent.com/69168575/140084143-9ae8a260-35f8-449f-9a05-003354d529bc.png)
