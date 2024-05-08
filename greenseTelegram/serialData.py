import serial
import schedule
import time
from datetime import datetime

nome_arquivo = 'dados_serial.txt'
MAX_TENTATIVAS_RECONEXAO = 5

def conectar_serial():
    portas = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']  # Lista de possíveis portas seriais

    for porta in portas:
        try:
            # Tenta estabelecer a conexão serial
            print("Tentando se conectar à porta serial", porta)
            ser = serial.Serial(porta, 9600, timeout=10)  # 9600 é a velocidade de transmissão, ajuste se necessário
            print("Conexão bem-sucedida com a porta serial", porta)
            return ser
        except serial.SerialException as e:
            print("Erro ao conectar à porta serial", porta, ":", e)
            continue

    print("Nenhuma porta serial disponível.")
    return None

def verificar_porta(ser):
    if ser is not None and ser.is_open:
        return True
    else:
        return False

def escrever_linha_arquivo(ser):
    if verificar_porta(ser):
        try:
            # Lê os dados da porta serial
            linha = ser.readline().strip()
            if linha:  # Verifica se a linha não está vazia
                # Obtém o horário atual
                # horario_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Formata a linha a ser escrita no arquivo
                linha_formatada = linha.decode('utf-8', errors='replace')
                print(linha_formatada)
                # Salva a linha formatada no arquivo
                with open(nome_arquivo, 'a', encoding='utf-8') as arquivo:
                    arquivo.write(linha_formatada + '\n')
        except serial.SerialException as e:
            print("Erro ao ler da porta serial:", e)
            # Tentar reconectar
            reconectar_serial(ser)
    else:
        print("Erro: Porta serial não está disponível.")
        # Tentar reconectar
        reconectar_serial(ser)

def reconectar_serial(ser):
    tentativas = 0
    while tentativas < MAX_TENTATIVAS_RECONEXAO:
        print("Tentando reconectar...")
        ser.close()
        ser = conectar_serial()
        if ser is not None:
            print("Reconexão bem-sucedida.")
            return
        tentativas += 1
        time.sleep(1)
    print("Não foi possível reconectar após", MAX_TENTATIVAS_RECONEXAO, "tentativas. Encerrando o programa.")
    exit(1)

def main():
    ser = conectar_serial()
    if ser is None:
        return

    # Agenda a execução da função para escrever a linha no arquivo a cada minuto
    schedule.every(10).seconds.do(escrever_linha_arquivo, ser)

    try:
        while True:
            # Executa as tarefas agendadas
            schedule.run_pending()
            time.sleep(1)
            # Verifica se a porta serial ainda está disponível
            if not verificar_porta(ser):
                print("Porta serial desconectada. Tentando reconectar...")
                reconectar_serial(ser)
                # Reagenda a tarefa com a nova conexão
                schedule.clear()
                schedule.every(10).seconds.do(escrever_linha_arquivo, ser)
    except KeyboardInterrupt:
        # Fecha a conexão serial quando o programa é interrompido
        ser.close()

if __name__ == "__main__":
    main()
