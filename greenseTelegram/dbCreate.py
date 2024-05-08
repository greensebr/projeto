import sqlite3
import os

os.remove("greenSe.db") if os.path.exists("greenSe.db") else None



db_locate = 'greenSe.db'


connie = sqlite3.connect(db_locate)
c = connie.cursor()

comando = """
CREATE TABLE estufa 
(ID INTEGER PRIMARY KEY AUTOINCREMENT, 
data_hora TIMESTAMP, 
periodo INTEGER, 
serial  INTEGER, 
painel INTEGER, 
rega INTEGER, 
soloT INTEGER, 
soloH INTEGER,
boiaB INTEGER,
boiaA INTEGER,
exaustor INTEGER, 
tempAtual INTEGER, 
tempAtiva INTEGER, 
umidAtual INTEGER, 
umidAtiva INTEGER)"""

c.execute(comando)

connie.commit()
connie.close()