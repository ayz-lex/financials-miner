import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

filename = "input.csv"

data = []

names = []

with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[2] == 'n/a' or row[3] == '0' or (len(row[0]) > 4):
            pass
        else:
            names.append(row[0])

for n in names:

    r = None
    status = True
    url = f'https://finance.yahoo.com/quote/{n}/key-statistics?p={n}'
    i = 0

    while status and i < 3:
        time.sleep(random.uniform(0, 1))
        r = requests.get(url)

        status = not (r.status_code == 200)
        i += 1

    try:
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')

        parsedData = soup.find(string="Valuation Measures").parent.parent.parent.parent

        dataContents = parsedData.contents
        valuationData = dataContents[0].find('table')
        fiscalHighlights = dataContents[2].find_all(class_="Pos(r)")
        tradingInformation = dataContents[1].find_all(class_="Pos(r)")

        # 'Ticker Symbol' (n), 'Quarterly Revenue Growth', 'Price Change (1 Year)', 
        # 'Profit Margin', 'Price/Sales', 'Price/Earnings', 'Price/Earnings Future', 
        # 'Book Value/Share', 'Market Cap'

        qrg = fiscalHighlights[3].find(string="Quarterly Revenue Growth").parent.parent.next_sibling.string
        ps = valuationData.find(string="Price/Sales").parent.parent.next_sibling.string
        pe = valuationData.find(string="Trailing P/E").parent.parent.next_sibling.string
        pef = valuationData.find(string="Forward P/E").parent.parent.next_sibling.string
        bv = fiscalHighlights[4].find(string="Book Value Per Share").parent.parent.next_sibling.string
        profit = fiscalHighlights[1].find(string="Profit Margin").parent.parent.next_sibling.string
        change = tradingInformation[0].find(string="52-Week Change").parent.parent.next_sibling.string
        mc = valuationData.find(string="Market Cap (intraday)").parent.parent.next_sibling.string

        data.append([n, qrg, ps, pe, pef, bv, profit, change, mc])

    except:
        
        print(f'Error on stock: {n}')

df = pd.DataFrame(data, columns=['Ticker', 'Quarterly Revenue Growth', 'Price/Sales', 'Trailing P/E', 'Forward P/E', 'Book Value', 'Profit Margin', '52-Week Change', 'Market Cap'])

df.to_csv('output.csv')