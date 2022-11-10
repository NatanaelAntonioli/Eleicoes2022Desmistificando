import pandas as pd

global df_pop 
df_pop = pd.read_csv("populacao.csv", delimiter=";")

def color(city):
    marcadas = ["RIO DE JANEIRO", "SÃO PAULO", "FORTALEZA", "BELO HORIZONTE", "CURITIBA", "BRASÍLIA", "RECIFE", "MANAUS", 
"PORTO ALEGRE", "GOIÂNIA", "BELÉM", "CAMPO GRANDE", "SÃO LUÍS", "TERESINA", "NOVA IGUAÇU", "MACEIÓ", "JOÃO PESSOA", "NATAL", "CUIABÁ", "FLORIANÓPOLIS"]

    if city in marcadas:
        return "Black"
    else:
        return "Red"


def get_populacao(city):
    lista = df_pop[df_pop.city == city]
    try:
        return(lista.iloc[0]['pop'])
    except:
        return -1

def to_int(valor):
    try:
        return int(valor)
    except:
        return -1