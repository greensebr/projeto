import sqlite3
import os

db_locate = 'greenSe.db'

connie = sqlite3.connect(db_locate)
c = connie.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS cultivo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        especie TEXT NOT NULL,
        dataInicio DATE NOT NULL,
        dataFinal DATE,
        horaInicio TIME NOT NULL,
        horaFinal TIME
    )
""")

# c.execute("ALTER TABLE cultivo ADD dataFinal DATE")
# c.execute("ALTER TABLE cultivo ADD horaFinal TIME")

# PRINTAR
c.execute("SELECT * FROM cultivo")
rows = c.fetchall()

c.execute("SELECT id FROM cultivo ORDER BY id DESC LIMIT 1")
last_id = c.fetchone()

#c.execute("DELETE FROM cultivo WHERE id=?", (last_id[0],))
connie.commit()

connie.close()

# Imprime os dados encontrados
for row in rows:
    print(f"ID: {row[0]}, Espécie: {row[1]}, Data: {row[2]}, Hora: {row[3]}")

if last_id:
    print(f"Último ID: {last_id[0]}")
