from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import matplotlib.pyplot as plt
import pandas as pd
import base64

app = Flask(__name__)
#app.static_folder = 'static/pics'

picFolder  = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
@app.route('/home')
def home_page():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'logo.png')
    data = query_estufa()
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'],'plot.png')
    return render_template('home.html', dataBase=data, user_image= pic1, user_image2= pic2)

# Rota para outra página
@app.route('/config', methods=["GET", "POST"])
def config():
    if request.method == 'POST':
        texto = request.form['texto']
        arquivo = open("./static/parametros.txt", "w")
        arquivo.write(texto)
        arquivo.close()

    pic1 = os.path.join(app.config['UPLOAD_FOLDER'],'logo.png')
    return render_template('config.html', ser_image3 = pic1)

db_locate = 'greenSe.db'

# Rota para newGrowth
@app.route('/admin/newGrowth', methods=["GET", "POST"])
def newGrowth():
    # two html pages: one for finishing the growth and another for starting a new one
    conn = sqlite3.connect(db_locate)
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM cultivo")
    last_id = c.fetchone()[0]

    c.execute("SELECT * FROM cultivo WHERE id = ?", (last_id,))
    row = c.fetchone()
    conn.close()

    if row:
        dataFinal = row[4]
        horaFinal = row[5]
    else:
        dataFinal = 1
        horaFinal = 1

    if dataFinal == None and horaFinal == None:
        if request.method == 'POST' and request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
            print ("Ainda não finalizou o cultivo")
            data = {
                'data': request.form['data'],
                'hora': request.form['hora'],
                'id': last_id
            }

            conn = sqlite3.connect(db_locate)
            c = conn.cursor()

            c.execute("UPDATE cultivo SET dataFinal = :data, horaFinal = :hora WHERE id = :id", data)
            conn.commit()
            conn.close()

            return redirect(url_for('home_page'))

        return render_template('finishGrowth.html', row=row)
        
    else:
        if request.method == 'POST' and request.form.get('username') == 'admin' and request.form.get('password') == 'admin':
            print ("Já finalizou o cultivo")
            data = {
                'especie': request.form['especie'],
                'data': request.form['data'],
                'hora': request.form['hora']
            }

            conn = sqlite3.connect(db_locate)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO cultivo (especie, data, hora) VALUES (:especie, :data, :hora)", data)
            conn.commit()
            cursor.execute("SELECT MAX(id) FROM cultivo")
            last_id = cursor.fetchone()[0]
            conn.close()

            return redirect(url_for('plot', id=last_id))

        return render_template('newGrowth.html')
   
# Rota para cada gráfico/cultivo
@app.route('/plot/<id>')
def plot(id):
    conn = sqlite3.connect(db_locate)
    c = conn.cursor()
    c.execute("SELECT * FROM cultivo WHERE id = ?", (id,))
    row = c.fetchone()
    print(row)
    conn.close()
    return render_template('plot.html', data=row)

def query_estufa():
    connie  = sqlite3.connect(db_locate)
    c = connie.cursor()
    comando = """SELECT * FROM estufa"""
    c.execute(comando)
    dados = c.fetchall()
    return dados

if __name__ == '__main__':
    app.run(host ='localhost', port = 5000, debug=True)
   # app.run(host ='192.168.0.200', port = 5000, debug=True)

