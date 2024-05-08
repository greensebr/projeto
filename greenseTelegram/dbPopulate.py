# Importações e definições de variáveis
import serial
import re
from datetime import datetime
import sqlite3
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def registro(data_hora, periodo, serial, painel, rega, soloT, soloH, boiaB, boiaA, exaustor, tempAtual, tempAtiva, umidAtual, umidAtiva):
    global c
    try:
        # Executando a inserção dos valores na tabela estufa
        c.execute('''INSERT INTO estufa 
                    (data_hora, periodo, serial, painel, rega, soloT, soloH, boiaB, boiaA, exaustor, tempAtual, tempAtiva, umidAtual, umidAtiva)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data_hora, periodo, serial, painel, rega, soloT, soloH, boiaB, boiaA, exaustor, tempAtual, tempAtiva, umidAtual, umidAtiva))
    except sqlite3.Error as e:
        print("Erro ao inserir dados no banco de dados:", str(e))

def plot_estufa(n):
    # Leitura dos parâmetros do arquivo
    with open("./static/parametros.txt", "r") as arquivo:
        parametros = arquivo.read()
    tpm, umm = parametros.split()[1], parametros.split()[2]
    #print(tpm, umm)
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
    df['data_hora'] = pd.to_datetime(df['data_hora'])

    # Cálculo dos valores de temperatura, umidade e umidade do solo
    last_row = df.iloc[-1]
    tp, um, tps, ums = f"{last_row['tempAtual']}/{tpm}C", f"{last_row['umidAtual']}/{umm}%", f"{last_row['soloT']}/30C", f"{last_row['soloH']}/50%"

    # Preparação dos dados para plotagem
    data_hora = df['data_hora'].to_numpy()
    periodo = df['periodo'].to_numpy()
    painel = df['painel'].to_numpy()
    rega = df['rega'].to_numpy()
    soloT = df['soloT'].to_numpy()
    soloH = df['soloH'].to_numpy()
    boiaB = 100*df['boiaB'].to_numpy()
    boiaA = 100*df['boiaA'].to_numpy()
    exaustor = df['exaustor'].to_numpy()
    tempAtual = df['tempAtual'].to_numpy()
    tempAtiva = df['tempAtiva'].to_numpy()
    umidAtual = df['umidAtual'].to_numpy()
    umidAtiva = df['umidAtiva'].to_numpy()


    # Configuração da figura e subplots
    fig, axs = plt.subplots(2, 1, figsize=(15, 10))

    # Plotagem do primeiro gráfico com temperatura e umidade
    axs[0].plot(data_hora, tempAtual, color='blue', label='TempAb')
   # axs[0].plot(data_hora, tempAtiva, color='blue', linestyle='--', label='Temp. Ativa')
    axs[0].plot(data_hora, umidAtual, color='green', label='UmidAb')
    #axs[0].plot(data_hora, umidAtiva, color='green', linestyle='--', label='Umid. Ativa')
    axs[0].plot(data_hora, soloT, color='magenta', label='TempSl')
    axs[0].plot(data_hora, soloH, color='black', label='UmidSl')
    axs[0].plot(data_hora, boiaB, color='magenta', linestyle='--',  label='boiaB')
    axs[0].plot(data_hora, boiaA, color='black', linestyle='--', label='boiaA')
    #axs[0].plot(data_hora, np.ones(len(data_hora)) * 50, color='black', linestyle='--', label='Umid. Solo Ativa')

    axs[0].set_xlabel('Tempo')
    axs[0].set_ylabel('Valores')
    axs[0].set_title(f'{n}: Gráfico de Temperatura e Umidade por Tempo - {str(last_row["data_hora"])[:19]}:{n}, {tp}, {um}, {tps}, {ums}')
    axs[0].legend(loc='upper left')
    axs[0].grid()

    # Plotagem do segundo gráfico com dados do painel e exaustor
    axs[1].plot(data_hora, painel+2.2, label='Painel')
    axs[1].plot(data_hora, exaustor+1.1, label='Exaustor')
    axs[1].plot(data_hora, rega, label='Rega')

    axs[1].set_xlabel('Tempo')
    axs[1].set_ylabel('Valores')
    axs[1].set_title(f'Gráfico do Painel ({str(periodo[-1])}) e Exaustor por Tempo - {str(last_row["data_hora"])[:19]}')
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

# Configurações para controle de transações
intervalo_commit = 10  # Número de inserções antes de fazer o commit
contador_commit = 0

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
        if (len(val.split()) == 27) and (val != ''):
            res = val.replace('\r\n', '').split(',')
            res = ''.join(res)
            posicoes = [match.start() for match in re.finditer(padrao, res)]
            vl = res[posicoes[-1]:].split()
            data = vl[1] + ' ' + vl[0]
            data_hora = datetime.now()
            periodo = vl[6]
            serial = vl[8]
            painel = vl[10]
            rega = vl[12]
            soloT = vl[14]
            soloH = vl[16]
            boiaB = vl[18]
            boiaA = vl[20]
            exaustor = vl[22]
            tempAtual = vl[24].split('/')[0]
            tempAtiva = vl[24].split('/')[1][:-2]
            umidAtual = vl[26].split('/')[0]
            umidAtiva = vl[26].split('/')[1][:-1]
            dados_atuais = (periodo, painel, rega, soloT, soloH, boiaB, boiaA, exaustor, tempAtual, tempAtiva, umidAtual, umidAtiva)

            # Verificar se os dados atuais são diferentes dos últimos dados registrados
            if dados_atuais != ultimos_dados:
                # Imprimir os dados atuais
                print(data_hora, periodo, painel, rega, soloT, soloH, boiaB, boiaA,exaustor, tempAtual, tempAtiva, umidAtual, umidAtiva)

                # Executar inserção
                registro(data_hora, periodo, serial, painel, rega, soloT, soloH, boiaB, boiaA, exaustor, tempAtual, tempAtiva, umidAtual,
                         umidAtiva)

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

n=0
# Loop principal
while True:
    try:

        ultimos_dados, contador_commit, n =  main(n, ultimos_dados, padrao, intervalo_commit, contador_commit)
    except Exception as e:
        print("Erro durante a execução:", str(e))
        try:
            # Inicialize a conexão com o Arduino
            arduino = serialArduino()
            ultimos_dados, contador_commit = main(n, ultimos_dados, padrao, intervalo_commit, contador_commit)
        except Exception as e:
            print("Erro Leitura função main :", str(e))
            sleep(5)

# Fechando a conexão com o banco de dados após o loop
connie.close()

