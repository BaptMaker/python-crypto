#coding: utf-8
#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from time import time, sleep
from send import Send
import json

def start():
    Cle = "3e2d124b-c93d-42e2-aa8c-bd9bb87a0c9e"

    print(" ____        _   _                        ____                  _        \n|  _ \ _   _| |_| |__   ___  _ __        / ___|_ __ _   _ _ __ | |_ ___  \n| |_) | | | | __| '_ \ / _ \| '_ \ _____| |   | '__| | | | '_ \| __/ _ \ \n|  __/| |_| | |_| | | | (_) | | | |_____| |___| |  | |_| | |_) | |_ (_) |\n|_|    \__, |\__|_| |_|\___/|_| |_|      \____|_|   \__, | .__/ \__\___/ \n       |___/                                        |___/|_|            ")

    print("\n [1]: Obtenir des information sur une crypto. \n [2]: Obtenir un fichier contenant toutes les crypto étudier. \n [3]: Lancer un serveur de surveillance de cypto.")
    choice = str(input("\n Choix: "))
    if choice == "1":
        symbol = input("\n Entrer le symbole de la crypto que vous souhaiter étudier: ")
        print("\n")
        a = createDic(Cle)

        etc = a[symbol.upper()]

        for keys, values in etc.items():
            print(" -",keys,":",values)
    
    elif choice == "2":

        a = createDic(Cle)

        file_name = str(datetime.now())

        fichier = open(file_name, "w")
        for Key, Values in a.items():
            fichier.write(f"\n -{Key}: {Values}\n")

        print("Dictionnaire Ok")
    
    elif choice == "3":
        Crypto = str(input("\nQuelle crypto souhaitez-vous étudier: "))
        Price = float(input("A quelle prix l'avez vous achetez: "))
        Prc = float(input("A quelle pourcentage souhaiter vous être prévenue: "))
        personal_time = int(input("A combien voulez vous régler l'interval de temps entre les vérification (en seconde): "))
        Numero= str(input("Veuiller entrer le numéro ou vous voulez être prévenue (Format: +33********* sans espaces): "))

        if " " in Numero == True:
            print("Vous avez entrer un numéro avec des espace.")
            start()
        elif "+33" in Numero == False:
            print("Vous n'avez pas respecter le format.")
            start()
        else:
            server(crypto=Crypto, price_buy=Price, pourcentage=Prc, TimePerso=personal_time, numero=Numero)


    choise = input("\n If you want to go to the menu press 's' and 'enter', else press 'enter'.")

    if choise == "s":
        start()
    else:
        exit()



def createDic(key):
    """ 
        Précondition: Prend une variable de type str contenant une clé d'API de CoinMarketCap

        Postcondition: Retourne un dictionnaire avec tout les crypto et des info dessus
    """
    NewDic = {}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'5000',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': key,
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)


      for i in range(len(data["data"])):
          mineable = ""

          if len(data["data"][i]["tags"]) >= 1:
              mineable = "Is mineable"
          else:
              mineable = "Doesn't mine this crypto."

          NewDic[data["data"][i]["symbol"]] = {"ID" : data["data"][i]["id"],"Name" : data["data"][i]["name"],"Price": f'{round(data["data"][i]["quote"]["USD"]["price"],2)}',"MarketCap" : data["data"][i]["quote"]["USD"]["market_cap"], "In circulation" : f'{round(data["data"][i]["circulating_supply"],1)} On {data["data"][i]["max_supply"]}', "Mineable" : mineable}
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    return NewDic

def server(price_buy, pourcentage, numero, crypto, TimePerso):
    Cle = "3e2d124b-c93d-42e2-aa8c-bd9bb87a0c9e"
    while True:
        dic = createDic(Cle)

        crypto_etudie = dic[crypto]

        calcMin = price_buy+(price_buy*pourcentage/100)

        if float(crypto_etudie["Price"]) >= calcMin:
            Send(f"÷nLe prix de la crypto {crypto} est a {crypto_etudie['Price']} USD \n Je pense que c'est le moment de vendre. \n \U0001F600", num=numero)

        else:
            print(crypto_etudie["Price"])

        sleep(TimePerso)





if __name__ == "__main__":
    start()