import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

planilha = "1t.csv"

def carrega_planilha(planilha_usar):
    df = pd.read_csv(planilha_usar, delimiter=";", encoding='latin1')
    #print(df)
    
    return df

# Tipos:
# 1 - QT_VOTOS_TOTAL_ACUMULADO
# 2 - PE_VOTOS_TOT_ACUMULADO

def make_line_plots(df, tipo, turno):
    #print(df)

    candidatos_primeiro_turno = ['CIRO_GOMES','LULA', 'PADRE_KELMON', 'SIMONE_TEBET', 'VERA', 'SOFIA_MANZANO', 'JAIR_BOLSONARO', 'CONSTITUINTE_EYMAEL', 'FELIPE_DAVILA', 'SORAYA_THRONICKE', 'LEO_PERICLES', 'BRANCO', 'NULO']
    candidatos_segundo_turno = ['LULA', 'JAIR_BOLSONARO', 'BRANCO', 'NULO']

    # Determina o turno

    candidatos = []

    if turno == 1:
        candidatos = candidatos_primeiro_turno
    else:
        candidatos = candidatos_segundo_turno

    # Determina o tipo de gráfico

    if tipo == 1:
        chave = '_QT_VOTOS_TOT_ACUMULADO'
    if tipo == 2:
        chave = '_PE_VOTOS_TOT_ACUMULADO'          

    candidatos = [x + chave for x in candidatos]
    candidatos.append('QT_VOTOS_TOTAL_ACUMULADO')

    df = df[candidatos]
    df = df.fillna(0)
    df.to_csv('final.csv', sep=";", encoding='latin1')
    print(df)

    df.set_index('QT_VOTOS_TOTAL_ACUMULADO').plot().legend(bbox_to_anchor=(1.0, 1.0))
    plt.show()

    #print(df)

    #plt.show()

df = carrega_planilha(planilha)
plt.legend(loc='upper left')
make_line_plots(df, 2,2)