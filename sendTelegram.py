import cv2
import asyncio
from telegram import Bot
import schedule
import time
from datetime import datetime
from selenium import webdriver

# Configuração do navegador
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Executar em modo headless (sem interface gráfica)
driver = webdriver.Chrome(options=options)  # Você precisa ter o chromedriver instalado e configurado no seu PATH

# Token de acesso do bot fornecido pelo BotFather
bot_token = '7004129631:AAGUGAIiDibjsoTa6Q4oDnU3R11IuGj2jLU'

# ID do chat para o qual deseja enviar a mensagem
chat_id = '-1002030305107'


# Função para capturar e enviar a foto
async def capturar_e_enviar_foto():


    try:
        # Carrega a página HTML
        driver.get('http://localhost:5000/')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Captura a screenshot da página
        screenshot_path = './static/pics/screenshot.png'
        driver.save_screenshot(screenshot_path)

        # Fecha o navegador
        driver.quit()

        print(f'Screenshot salvo em: {screenshot_path}')
    except:
        print('Print de página HTML')


    # Inicializa a webcam
    cap = cv2.VideoCapture(0)

    # Verifica se a webcam foi aberta corretamente
    if not cap.isOpened():
        print("Erro ao abrir a webcam")
        return

    # Captura uma imagem da webcam
    ret, frame = cap.read()

    # Verifica se a captura foi bem-sucedida
    if not ret:
        print("Erro ao capturar a imagem")
        return

    # Salva a imagem em um arquivo temporário
    cv2.imwrite("./static/pics/imagem_webcam.jpg", frame)

    # Libera a webcam
    cap.release()

    # Mensagem que deseja enviar junto com a imagem

    # Obtém a hora atual
    hora_atual = datetime.now()

   # print("Hora atual:", )

    mensagem = 'Foto: '+str(hora_atual)[:19]

    # Cria uma instância do bot
    bot = Bot(token=bot_token)

    # Envia a mensagem ao chat especificado com a foto
    await bot.send_photo(chat_id=chat_id, photo=open('./static/pics/imagem_webcam.jpg', 'rb'))
    await bot.send_photo(chat_id=chat_id, photo=open("./static/pics/plot.png", 'rb'), caption=mensagem)

# Função wrapper para chamar a função assíncrona no loop de eventos asyncio
def wrapper():
    asyncio.run(capturar_e_enviar_foto())


# Agendamento da execução da função a cada minuto
schedule.every(6*60*60).seconds.do(wrapper)

# Loop para manter o programa em execução
#k=0
while True:
    try:
        schedule.run_pending()
        time.sleep(1)
       # k+=1
       # print('Foto:',k)
    except:
        print('Erro')






