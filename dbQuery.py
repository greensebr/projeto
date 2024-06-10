import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from time import sleep
import numpy as np


db_locate = 'greenSe.db'

connie = sqlite3.connect(db_locate)
c = connie.cursor()

comando = """SELECT * FROM estufa"""
c.execute(comando)
dados = c.fetchall()
# Nome da tabela que você quer visualizar
table_name = 'estufa'  # Substitua 'pessoas' pelo nome da sua tabela

# Consulta para obter informações das colunas da tabela
query = f"PRAGMA table_info({table_name})"
c.execute(query)
columns_info = c.fetchall()
# Exibir o nome e o tipo de cada coluna
df = pd.DataFrame(dados, columns=[c[1] for c in columns_info]).set_index('ID')#.plot(figsize=(10, 5))
#df['data_hora'] = pd.to_datetime(df['data_hora'])
#print(df)
#df.plot()
def plot_estufa():

    arquivo = open("./static/parametros.txt", "r")
    paramentros = arquivo.read()

    tpm = paramentros.split()[1]
    umm = paramentros.split()[2]
#    print(tpm, umm)
    arquivo.close()

    connie  = sqlite3.connect(db_locate)
    c = connie.cursor()
    comando = """SELECT * FROM estufa"""
    c.execute(comando)
    dados = c.fetchall()
    # Nome da tabela que você quer visualizar
    table_name = 'estufa'  # Substitua 'pessoas' pelo nome da sua tabela

    # Consulta para obter informações das colunas da tabela
    query = f"PRAGMA table_info({table_name})"
    c.execute(query)
    columns_info = c.fetchall()
    # Exibir o nome e o tipo de cada coluna
    df = pd.DataFrame(dados, columns=[c[1] for c in columns_info]).set_index('ID')  # .plot(figsize=(10, 5))
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    print(df.iloc[-1])

    tp, um, ums = str(df.iloc[-1]['tempAtual']) +'/'+tpm+'C', str(df.iloc[-1]['umidAtual']) +'/'+umm+'%', str(df.iloc[-1]['solo']) +'/50%'

    # Convertendo as colunas para arrays do Numpy
    data_hora = df.data_hora.to_numpy()
    periodo = df.periodo.to_numpy()

    painel = df.painel.to_numpy()
    solo = df.solo.to_numpy()
    exaustor = df.exaustor.to_numpy()
    tempAtual = df.tempAtual.to_numpy()
    tempAtiva = df.tempAtiva.to_numpy()
    umidAtual = df.umidAtual.to_numpy()
    umidAtiva = df.umidAtiva.to_numpy()



    # Criando uma figura com dois subplots em uma linha
    fig, axs = plt.subplots(2, 1, figsize=(15, 10))

    # Plotando o primeiro gráfico no primeiro eixo
    # Plotando o primeiro gráfico no primeiro eixo com escala logarítmica em y
    axs[0].plot(data_hora, tempAtual, color='blue', label='Temp. Atual')
    axs[0].plot(data_hora, tempAtiva, color='blue', linestyle='--', label='Temp. Ativa')
    axs[0].plot(data_hora, umidAtual, color='green', label='Umid. Atual')
    axs[0].plot(data_hora, umidAtiva, color='green', linestyle='--', label='Umid. Ativa')
    axs[0].plot(data_hora, solo, color='black', label='Umid. Solo')
    axs[0].plot(data_hora, np.ones(len(data_hora))*50, color='black', linestyle='--', label='Umid. Solo Ativa')

    axs[0].set_xlabel('Tempo')
    axs[0].set_ylabel('Valores')
    axs[0].set_title('Gráfico de Temperatura e Umidade por Tempo - '+str(df['data_hora'].iloc[-1])[:19]+': '+tp+', '+um+', '+ums)
    axs[0].legend()
    axs[0].grid()
    # axs[0].set_yscale('log')  # Aplicando escala logarítmica no eixo y

    # Plotando o segundo gráfico no segundo eixo
  # axs[1].plot(data_hora, serial, label='Serial')
    axs[1].plot(data_hora, painel, label='Painel')
    axs[1].plot(data_hora, exaustor, label='Exaustor')
    axs[1].set_xlabel('Tempo')
    axs[1].set_ylabel('Valores')
    axs[1].set_title('Gráfico do Painel ('+str(periodo[-1])+') e Exaustor por Tempo - '+str(df['data_hora'].iloc[-1])[:19])
    axs[1].legend()
    axs[1].grid()
    # Ajustando o espaçamento entre os subplots
    plt.tight_layout()

    plt.savefig("./static/pics/plot.png")
    plt.close()


while True:

    sleep(10)
  #  try:
    plot_estufa()
  #  except:
  #      print('Erro')