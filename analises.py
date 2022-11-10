import pandas as pd
import matplotlib.pyplot as plt
from aux_analises import *
import numpy as np

planilha = "2018.csv"
planilha_locais = "eleitorado_local_votacao_2022.csv"
planilha_populacao = "populacao.csv"

if planilha == "2018.csv":
    esquerda = "FERNANDO HADDAD"
    direita = "JAIR BOLSONARO"

else:
    esquerda = "LULA"
    direita = "JAIR BOLSONARO"


def carrega_planilha(planilha_usar):
    df = pd.read_csv(planilha_usar, delimiter=";", encoding='latin1')
    df["Color"] = ""
    df["Color"] = df['NM_MUNICIPIO'].apply(color)
    try:
        df["Populacao"] = df['Populacao'].apply(to_int)
    except:
        pass
    #df["Populacao"] = df['NM_MUNICIPIO'].apply(get_populacao) # Não mais necesário, pois o arquivo já tem as populações
    print(df)
    #df.to_csv('final.csv', sep=";", encoding='latin1') # Não mais necessário, pois o arquivo já tem as populações
    return df

def carrega_locais(planilha_usar):
    df = pd.read_csv(planilha_usar, delimiter=";", encoding='latin1')
    return df

def grafico_pizza_urna(df):
    df1 = df['NR_URNA_EFETIVADA'].value_counts()
    a = df1.plot(kind='pie')
    plt.show()

def grafico_dispersao_ano(df, ano):

    df_20 = df[df.NR_URNA_EFETIVADA == ano]

    a = df_20.plot.scatter(x=direita, y=esquerda,c='DarkBlue', s=2)
    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.show()


def lista_cidades_urna_2020(df):
    df_current = df[df.NR_URNA_EFETIVADA == 2020]
    df_current = df_current[df.SG_UF == 'CE']
    df_current = df_current[df.Populacao < 50000]
    df1 = df_current['NM_MUNICIPIO'].value_counts()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df1)

def grafico_dispersao_urnas_cidade(df):

    df_current = df[df.NM_MUNICIPIO == 'RIO DE JANEIRO']

    a = df_current.plot.scatter(x=direita, y=esquerda,c='DarkBlue', s=2)
    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.show()

def grafico_dispersao_cidades(df):

    a = df.plot.scatter(x=direita, y=esquerda,c='Color', s=2)
    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.show()

def grafico_dispersao_geral(df):

    a = df.plot.scatter(x=direita, y=esquerda,c='DarkBlue', s=2)
    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.show()

def localiza_secao (municipio, zona, secao, locais):

    lista = locais[locais.NM_MUNICIPIO == municipio]
    lista = lista[lista.NR_ZONA == zona]
    lista = lista[lista.NR_SECAO == secao]
    lista = lista[lista.NR_TURNO == 2]

    for index, row in lista.iterrows():
        return(municipio + ", zona " + str(zona) + ", seção " + str(secao) + ", " + row['DS_ENDERECO'])

def endereco_zero_votos(df, locais):
    lista = df.loc[df['JAIR BOLSONARO'] == 0]
    print("Total de " + str(lista[esquerda].sum()) + " votos para o PT.")

    for index, row in lista.iterrows():
        try:
            print(localiza_secao(row['NM_MUNICIPIO'], row['NR_ZONA'], row['NR_SECAO'], locais) + " com " + str(row[esquerda]) + " votos para o PT")
        except:
            pass
    print(lista)

def total_votos_limiar(df,limiar):
    lista = df.loc[df['LULA']/(df['JAIR BOLSONARO']+ df['LULA']) >= 0.98]
    print("Total de " + str(lista[esquerda].sum()) + " votos para o PT.")


def compara_estado_urnas(df, estado, limite):
    df_current = df[df.SG_UF == estado]
    df_current = df_current[df.Populacao <= limite]

    anos = [2009, 2010, 2011, 2013, 2015, 2020, 0]

    print("|AnoM|Hadd|Bols|Diff|")
    for ano in anos:
        if ano != 0:
            df_urnas = df_current[df.NR_URNA_EFETIVADA == ano]
        else:
            df_urnas = df_current[df.NR_URNA_EFETIVADA != 2020]
        Total_lula = df_urnas[esquerda].sum()
        Total_bolsonaro = df_urnas[direita].sum()

        fracao_lula = (Total_lula/(Total_lula + Total_bolsonaro))*100
        fracao_bolsonaro = (Total_bolsonaro/(Total_lula + Total_bolsonaro))*100
        
        
        if ano != 0:

            print ("|" + str(ano) + "|" + str(round(fracao_lula,1)) + "|" + str(round(fracao_bolsonaro,1)) + "|" + str(round(fracao_bolsonaro,1)) + "|")
            #print("Em urnas do ano " + str(ano) + ", Lula teve " + str(round(fracao_lula,1)) +  " e Bolsonaro teve " + str(round(fracao_bolsonaro,1)) + " com diferença de " + str(round(fracao_lula - fracao_bolsonaro,1)))
        else:
            print ("|Ante|" + str(round(fracao_lula,1)) + "|" + str(round(fracao_bolsonaro,1)) + "|" + str(round(fracao_bolsonaro,1)) + "|")

            #print("Em modelo anterior" + ", Lula teve " + str(round(fracao_lula,1)) +  " e Bolsonaro teve " + str(round(fracao_bolsonaro,1)) + " com diferença de " + str(round(fracao_lula - fracao_bolsonaro,1)))


def compara_estados_região(df):

    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL','SE', 'BA']

    for estado in nordeste:
        print("------------------------  " + estado + "  ------------------------")
        compara_estado_urnas(df, estado, 50000)

def benford_secoes(df):
    
    controle = 'QT_COMPARECIMENTO'

    df[esquerda] = df[esquerda].astype(str).str[0].astype(int)
    df[direita] = df[direita].astype(str).str[0].astype(int)
    df[controle] = df[controle].astype(str).str[0].astype(int)

    hist_esquerda = df[esquerda].value_counts()
    hist_direita = df[direita].value_counts()
    hist_quorum = df[controle].value_counts()

    print("Para os votos da esquerda:")
    print(hist_esquerda)
    print("Para os votos da direita:")
    print(hist_direita)
    print("Para os comparecidos:")
    print(hist_quorum)

def get_total_votos_cidade(nome_municipio, df):

    lista = df.loc[df['NM_MUNICIPIO'] == nome_municipio]
    soma_esquerda = lista[esquerda].sum()
    soma_direita = lista[direita].sum()

    return [soma_esquerda, soma_direita]

def benford_cidades(df):
    array = df['NM_MUNICIPIO'].unique()
    print(array)

    df_benford = pd.DataFrame({'Cidade': array, 'VotosEsq': 0, 'VotosDir' :0})

    for index in df_benford.index:
        tupla = get_total_votos_cidade(df_benford['Cidade'][index],df)
        df_benford['VotosEsq'][index] = df_benford['VotosEsq'][index] + tupla[0]
        df_benford['VotosDir'][index] = df_benford['VotosDir'][index] + tupla[1]
        print (index)

    print(df_benford)

    df_benford['VotosEsq'] = df_benford['VotosEsq'].astype(str).str[0].astype(int)
    df_benford['VotosDir'] = df_benford['VotosDir'].astype(str).str[0].astype(int)

    hist_esquerda = df_benford['VotosEsq'].value_counts(normalize=True)
    hist_direita = df_benford['VotosDir'].value_counts(normalize=True)

    print("Para os votos da esquerda:")
    print(hist_esquerda)
    print("Para os votos da direita:")
    print(hist_direita)

    hist_esquerda = df_benford['VotosEsq'].value_counts()
    hist_direita = df_benford['VotosDir'].value_counts()

    print("Para os votos da esquerda:")
    print(hist_esquerda)
    print("Para os votos da direita:")
    print(hist_direita)

df = carrega_planilha(planilha)
#df_locais = carrega_locais(planilha_locais)

benford_cidades(df)

#total_votos_limiar(df, 0.98)
#df_locais = carrega_locais(planilha_locais)
#endereco_zero_votos(df, df_locais)