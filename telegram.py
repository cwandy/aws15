import requests
TOKEN = "6643079698:AAHNhVI3kRc8DKoBS5SE1lFixFCr5S6Nd4A"
chat_id = "1256404467"

def sendme(message):
    msg = message
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={msg}"
    requests.get(url).json() # this sends the message