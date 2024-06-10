# Importações e definições de variáveis
import serial
import re
from datetime import datetime
import sqlite3
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def registro(DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta):
    global c
    try:
        # Executando a inserção dos valores na tabela estufa
        c.execute('''INSERT INTO estufa 
                    (DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta))
    except sqlite3.Error as e:
        print("Erro ao inserir dados no banco de dados:", str(e))

def plot_estufa(n):
    # Leitura dos parâmetros do arquivo
    with open("./static/parametros.txt", "r") as arquivo:
        parametros = arquivo.read()
    tpm, umm = parametros.split()[1], parametros.split()[2]
    print(tpm, umm)
    #tpm, umm = 10, 10
    # Conexão com o banco de dados SQLite e obtenção dos dados da tabela estufa
    connie = sqlite3.connect(db_locate)
    c = connie.cursor()
    c.execute("SELECT * FROM estufa")
    dados = c.fetchall()

    # Criação do DataFrame a partir dos dados do banco
    columns_info = c.execute("PRAGMA table_info(estufa)").fetchall()
    column_names = [c[1] for c in columns_info]
    df = pd.DataFrame(dados, columns=column_names).set_index('ID')
    df['DataHora'] = pd.to_datetime(df['DataHora'])


    # Preparação dos dados para plotagem
    Amostra = range(len(df['DataHora']))
    Periodo = df['Periodo'].to_numpy()
    Serial = df['Serial'].to_numpy()
    Painel = df['Painel'].to_numpy()
    Exaustor = df['Exaustor'].to_numpy()
    TempAmb = df['TempAmb'].to_numpy()
    UmidAmb = df['UmidAmb'].to_numpy()
    TempSolo = df['TempSolo'].to_numpy()
    UmidSolo = df['UmidSolo'].to_numpy()
    BoiaBaixa = df['BoiaBaixa'].to_numpy()
    BoiaAlta = df['BoiaAlta'].to_numpy()

    # Configuração da figura e subplots
    fig, axs = plt.subplots(2, 1, figsize=(15, 10))

    # Plotagem do primeiro gráfico com temperatura e umidade
    axs[0].plot(Amostra, TempAmb, color='blue', label='TempAb')
    axs[0].plot(Amostra, UmidAmb, color='green', label='UmidAb')
    axs[0].plot(Amostra, TempSolo, color='magenta', label='TempSl')
    axs[0].plot(Amostra, UmidSolo, color='black', label='UmidSl')

    #axs[0].set_xlabel('Amostras')
    axs[0].set_ylabel('Valores')

    # Cálculo dos valores de temperatura, umidade e umidade do solo
    tempo_atual = datetime.now()

    axs[0].set_title(f'Imagem: {n}, Tempo: {str(tempo_atual)[:-10]}, TempAmb: {TempAmb[-1]}°C, UmidAmb: {UmidAmb[-1]}%, TempSolo: {TempSolo[-1]}°C, UmidSolo: {UmidSolo[-1]}%')
    axs[0].legend(loc='upper left')
    axs[0].grid()

    # Plotagem do segundo gráfico com dados do painel e exaustor
    axs[1].plot(Amostra, Painel+2.2, label='Painel')
    axs[1].plot(Amostra, Exaustor+1.1, label='Exaustor')
    axs[1].plot(Amostra, BoiaBaixa, color='magenta', linestyle='--', label='boiaB')
    axs[1].plot(Amostra, BoiaAlta, color='black', linestyle='--', label='boiaA')

    axs[1].set_xlabel('Amostras')
    axs[1].set_ylabel('Valores')
    axs[1].set_title(f'Imagem: {n}, Painel: {Painel[-1]}, Exaustor: {Exaustor[-1]}, BoiaBaixa: {BoiaBaixa[-1]}, BoiaAlta: {BoiaAlta[-1]}')

   #axs[1].set_title(f'Gráfico do Painel ({str(periodo[-1])}) e Exaustor por Tempo - {str(last_row["data_hora"])[:19]}')
    axs[1].legend(loc='upper left')
    axs[1].grid()

    # Ajuste do espaçamento entre os subplots
    plt.tight_layout()

    # Salvando o gráfico como imagem e fechando a figura
    plt.savefig("./static/pics/plot.png")
    plt.close()



# Defina a porta serial correta do seu Arduino
def serialArduino():
    # Inicialize a conexão com o Arduino
    try:
        porta_serial = '/dev/ttyACM0'
        arduino = serial.Serial(porta_serial, baudrate=9600, timeout=1)
        print("Conexão com o Arduino estabelecida!" + porta_serial)
    except serial.SerialException as e:
        porta_serial = '/dev/ttyACM1'
        arduino = serial.Serial(porta_serial, baudrate=9600, timeout=1)
        print("Conexão com o Arduino estabelecida!" + porta_serial)
        print("Erro ao conectar ao Arduino:", str(e))
    return arduino

arduino = serialArduino()
print(arduino)

# Conexão com o banco de dados SQLite
db_locate = 'greenSe.db'
connie = sqlite3.connect(db_locate)
c = connie.cursor()

# Variáveis para armazenar os últimos dados registrados
ultimos_dados = None

# Padrao e variáveis de controle
padrao = r'\b\d{1,2}:\d{2}:\d{2} \d{2}/\d{2}/\d{4}\b'


# Loop principal

def main(n, ultimos_dados, padrao, intervalo_commit, contador_commit):
    arquivo = open("./static/parametros.txt", "r")
    paramentros = arquivo.read()
    # print(paramentros)
    arduino.write(paramentros.encode())
    arquivo.close()
    sleep(3)
    try:
        val = str(arduino.readline().decode())
        #print(val.split(), len(val.split()))
        if (len(val.split()) == 25) and (val != ''):
            res = val.replace('°C', '').replace('%', '').split(',')
            Valores = ''.join(res).split()
      #      print(Valores)
            DataHora =  Valores[1]+' '+Valores[0]
            Periodo = Valores[6]
            Serial = Valores[8]
            Painel = Valores[10]
            Exaustor = Valores[12]
            TempAmb = Valores[14]
            UmidAmb = Valores[16]
            TempSolo = Valores[18]
            UmidSolo = Valores[20]
            BoiaBaixa = Valores[22]
            BoiaAlta = Valores[24]
            #print(DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta)
            dados_atuais = (Periodo, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta)
            # Verificar se os dados atuais são diferentes dos últimos dados registrados
            if dados_atuais != ultimos_dados:
                # Imprimir os dados atuais
                print('DataHora: ', DataHora, ', Periodo: ', Periodo, ', Painel: ', Painel,', Exaustor: ', Exaustor,', TempAmb: ',
                      TempAmb, ', UmidAmb: ', UmidAmb, ', TempSolo: ', TempSolo, ', UmidSolo: ', UmidSolo, ', BoiaBaixa: ', BoiaBaixa, ', BoiaAlta: ', BoiaAlta)
               # Executar inserção
                registro(DataHora, Periodo, Serial, Painel, Exaustor, TempAmb, UmidAmb, TempSolo, UmidSolo, BoiaBaixa, BoiaAlta)

                # Atualizar os últimos dados registrados
                ultimos_dados = dados_atuais

                # Incrementar o contador de inserções
                contador_commit += 1

                # Fazer o commit da transação se necessário
                if contador_commit >= intervalo_commit:
                    n += 1
                    connie.commit()  # Fazer o commit da transação
                    contador_commit = 0  # Reiniciar o contador
                    print("Fazendo commit()!")
                    plot_estufa(n)
        return ultimos_dados, contador_commit, n

    except Exception as e:

        print("Erro durante a execução Interna:", str(e))


# Configurações para controle de transações
intervalo_commit = 10  # Número de inserções antes de fazer o commit
contador_commit = 0
n = 0


while True:
    try:
        ultimos_dados, contador_commit, n =  main(n, ultimos_dados, padrao, intervalo_commit, contador_commit)
        sleep(3)
    except Exception as e:
        arduino = serialArduino()
        print("Erro durante a execução:", str(e))
connie.close()
