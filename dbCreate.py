import sqlite3
import os

# pq apagar o banco de dados?
os.remove("greenSe.db") if os.path.exists("greenSe.db") else None

db_locate = 'greenSe.db'

connie = sqlite3.connect(db_locate)
c = connie.cursor()

create_table_cultivo = """
    CREATE TABLE IF NOT EXISTS cultivo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        especie TEXT NOT NULL,
        dataInicio DATE NOT NULL,
        dataFinal DATE,
        horaInicio TIME NOT NULL,
        horaFinal TIME
    )
"""

# c.execute(create_table_cultivo)

create_table_estufa = """
    CREATE TABLE estufa (
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
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
        BoiaAlta INTEGER,
        FOREIGN KEY (ID) REFERENCES cultivo(id)
    )
"""

c.execute(create_table_estufa)

connie.commit()
connie.close()