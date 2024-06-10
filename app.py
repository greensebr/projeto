from flask import Flask, render_template, request
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

