import sqlite3
import os

os.remove("greenSe.db") if os.path.exists("greenSe.db") else None



db_locate = 'greenSe.db'


connie = sqlite3.connect(db_locate)
c = connie.cursor()

comando = """
CREATE TABLE estufa 
(ID INTEGER PRIMARY KEY AUTOINCREMENT, 
DataHora TIMESTAMP, 
Periodo INTEGER, 
Serial  INTEGER, 
Painel INTEGER, 
Exaustor INTEGER, 
TempAmb INTEGER,
UmidAmb INTEGER,
TempSolo INTEGER,
UmidSolo INTEGER, 
BoiaBaixa INTEGER, 
BoiaAlta INTEGER)"""

c.execute(comando)

connie.commit()
connie.close()