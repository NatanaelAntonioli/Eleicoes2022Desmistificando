# Esse código recebe um link e um turno, e baixa/extrai todos os boletins de urna desse turno
# Em seguida, junta todos os cvs em um só.

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests

from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import os
import glob
import pandas as pd
import numpy as np

from aux import *

import functools as ft

turno = "2t"
url = 'https://dadosabertos.tse.jus.br/dataset/resultados-2018-boletim-de-urna'

def baixa_csvs():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla'})

    reqs = session.get(url)
    
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    urls = []
    for link in soup.find_all('a'):
        if ".zip" in link.get('href') and "sha512" not in link.get('href') and turno in link.get('href'):
            baixar = link.get('href')
            print(baixar)
            with urlopen(Request(baixar, headers={'User-Agent': 'Mozilla'})) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall()

def une_csvs():
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    print(all_filenames)
    
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f, delimiter=";", encoding='latin1') for f in all_filenames ])
    #export to csv
    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='latin1', sep=';')

def produz_tratado():

    df = pd.read_csv("combined_csv.csv", delimiter=";", encoding='latin1')
    df = df[df.DS_CARGO_PERGUNTA == "Presidente"]

    #print(df)
    unicos_candidatos = df["NM_VOTAVEL"].unique()

    dfs = []

    contador = 0
    for candidato in unicos_candidatos:
        temp = df[df.NM_VOTAVEL == candidato]
        temp = temp[['SG_UF','NM_MUNICIPIO', 'NR_ZONA', 'NR_SECAO', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ABSTENCOES', 'NR_URNA_EFETIVADA', 'QT_VOTOS']]
        temp = temp.rename({'QT_VOTOS': candidato}, axis='columns')
        
        dfs.append(temp)
        contador = contador + 1

    df_final = dfs[0]
    df_final = df_final.merge(dfs[1], how = "left")
    df_final = df_final.merge(dfs[2], how = "left")
    df_final = df_final.merge(dfs[3], how = "left")

    df_final = df_final.drop_duplicates()
    df_final = df_final.fillna(0)

    df_final.to_csv('final.csv', sep=";", encoding='latin1')

def estabelece_modelo():
    df = pd.read_csv("final.csv", delimiter=";", encoding='latin1')
    contador = 0
    
    df['NR_URNA_EFETIVADA'] = df['NR_URNA_EFETIVADA'].apply(modelo_urna)

    df.to_csv('final.csv', sep=";", encoding='latin1')

baixa_csvs()
une_csvs()
produz_tratado()
estabelece_modelo()
