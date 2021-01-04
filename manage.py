import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random

filename = "input.csv"

data = []

# 7 ipo year

with open(filename) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[2] == 'n/a' or row[3] == '0' or (len(row[0]) > 4) or float(row[5]) < 300000000:
            pass
        else:
            data.append([row[0], row[7]])

i = 0
while i < len(data):

    row = data[i]

    n = row[0]

    r = None
    status = True
    url = f'https://finance.yahoo.com/quote/{n}/key-statistics?p={n}'

    r = requests.get(url, headers = {'User-agent': 'Super Bot Power Level Over 9000'})

    # while status and i < 3:
    #     time.sleep(random.uniform(0, 1))
    #     r = requests.get(url)

    #     status = not (r.status_code == 200)
    #     i += 1

    try:
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')

        parsedData = soup.find(string="Valuation Measures").parent.parent.parent.parent

        dataContents = parsedData.contents
        #valuationData = dataContents[0].find('table')
        fiscalHighlights = dataContents[2].find_all(class_="Pos(r)")
        tradingInformation = dataContents[1].find_all(class_="Pos(r)")

        # 'Ticker Symbol' (n), 'Quarterly Revenue Growth', 'Price Change (1 Year)', 
        # 'Profit Margin', 'Price/Sales', 'Price/Earnings', 'Price/Earnings Future', 
        # 'Book Value/Share', 'Market Cap'

        qrg = fiscalHighlights[3].find(string="Quarterly Revenue Growth").parent.parent.next_sibling.string
        #ps = valuationData.find(string="Price/Sales").parent.parent.next_sibling.string
        #pe = valuationData.find(string="Trailing P/E").parent.parent.next_sibling.string
        #pef = valuationData.find(string="Forward P/E").parent.parent.next_sibling.string
        bv = fiscalHighlights[4].find(string="Book Value Per Share").parent.parent.next_sibling.string
        profit = fiscalHighlights[1].find(string="Profit Margin").parent.parent.next_sibling.string
        change = tradingInformation[0].find(string="52-Week Change").parent.parent.next_sibling.string
        #mc = valuationData.find(string="Market Cap (intraday)").parent.parent.next_sibling.string

        #data.append([n, qrg, ps, pe, pef, bv, profit, change, mc])
        row.extend([qrg, bv, profit, change])
        i += 1
    except:
        del data[i]
        print(f'Error: {n}')

def sort_func(element):
    if element[2] == 'N/A':
        return float('inf')
    else:
        res = 0.0

        try:
            res = float(element[2][:-1])
        except:
            res = float('inf')

        return res

data.sort(key = sort_func)

#df = pd.DataFrame(data, columns=['Ticker', 'Quarterly Revenue Growth', 'Price/Sales', 'Trailing P/E', 'Forward P/E', 'Book Value', 'Profit Margin', '52-Week Change', 'Market Cap'])
df = pd.DataFrame(data, columns=['Ticker', 'IPO Year', 'Quarterly Revenue Growth', 'Book Value', 'Profit Margin', '52-Week Change'])

df.to_csv('output.csv')