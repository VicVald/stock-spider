import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt

def conversor(value):
    url = "https://www.google.com/finance/markets/currencies?hl=pt"

    plain_text = requests.get(url).text
    soup = BeautifulSoup(plain_text, "html.parser")
    brl_to = soup.find_all("span", class_="JLPHhb")
    i = value
    if i == 0:
        usd = brl_to[0].text#USD = 0
        if"," in usd:
            usd = usd.replace(",", ".")    
            return float(usd)
    elif i == 1:
        eur = brl_to[1].text#EUR = 1
        if"," in eur:
            eur = eur.replace(",", ".")    
            return float(eur)
    elif i == 2:
        gbp = brl_to[2].text#GBP = 2
        if"," in gbp:
            gbp = gbp.replace(",", ".")    
            return float(gbp)
    elif i == 3:
        jpy = brl_to[3].text#JPY = 3
        if"," in jpy:
            jpy = jpy.replace(",", ".")    
            return float(jpy)
    elif i == 4:
        aud = brl_to[4].text#AUD = 3
        if"," in aud:
            aud = aud.replace(",", ".")    
            return float(aud)

def get_price(url):
    try:
        plain_text = requests.get(url).text
        soup = BeautifulSoup(plain_text, "html.parser")
        price = soup.find("div", class_="YMlKec fxKbKc").text
        #convert to float
        if "R$" in price:
            price = price.replace("R$", "").replace(",", ".").strip()
            price = float(price)
        return price
    except AttributeError or requests.exceptions.ConnectionError:
        return "Error"

        
def counters(file, index):
        #counters
        coinMax = 0
        coinMin = 0
        lastCoin = 0
        date_coinMax = None
        date_coinMin = None
        with open(file, 'r') as table:
            csv_reader = csv.reader(table)
            next(csv_reader)
            for row in csv_reader:
                coin = (row[index].strip())
                lastCoin = coin
                if any(char.isalpha() for char in coin):
                    continue
                if coinMax == 0 or coinMax < coin:
                        coinMax = coin
                        date_coinMax = row[0]
                if coinMin == 0 or coinMin > coin:
                        coinMin = coin
                        date_coinMin = row[0]
        table.close()
        return date_coinMax, coinMax, date_coinMin, coinMin, lastCoin

def create_graph(table, index, acronym):
    with open(table, 'r') as table:
        csv_reader = csv.reader(table)
        next(csv_reader)
        plt.figure(figsize=(50, 25))

        times = []
        values = []

        for row in csv_reader:
            times.append(datetime.strptime(row[0], "%H:%M:%S"))
            values.append(float(row[index].strip()))
            plt.plot(times, values)
        plt.xlabel("Hora")
        plt.ylabel("Preço")
        plt.title(f"Preço do {acronym.strip()}")
        #plt.show()

def date():
    actualTime = datetime.now().strftime("%H:%M:%S")
    return actualTime

def date_day():
    actualTime = datetime.now().strftime("%D")
    return actualTime

def end():
    actualTime = datetime.now().strftime("%H")
    actualTime = int(actualTime)
    if actualTime >= 17 or actualTime < 10:
        return True