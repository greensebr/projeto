import sqlite3
from time import sleep

db_locate = 'greenSe.db'

def main (n, ultimos_dados, contador_commit, intervalo_commit):
    print ("Iniciando a execução")
    return n, ultimos_dados, contador_commit

n = 0
ultimos_dados = None
contador_commit = 0

while True:
    conn = sqlite3.connect(db_locate)
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM cultivo")
    last_id = c.fetchone()[0]
    if last_id == None:
        break
    c.execute("SELECT dataFinal FROM cultivo WHERE id = ?", (last_id,))
    dataFinal = c.fetchone()[0]

    intervalo_commit = 10

    if dataFinal == None:
        # try:
        n, ultimos_dados, contador_commit =  main(n, ultimos_dados, contador_commit, intervalo_commit)
        # except Exception as e:
        #     arduino = serialArduino()
        #     print("Erro durante a execução:", str(e))

    else:
        print ("Não tem plantação ativa")
        n = 0
        ultimos_dados = None
        contador_commit = 0

    sleep(3)

