from Stock import Stock
import re
import ssl
import random
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd

def out(df):
    df.to_csv('output.csv')

def main():
    filename = "companylist2.csv"

    cols = dict()

    names = list()

    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ',')
        for row in readCSV:
            if row[2] == 'n/a' or row[3] == '0' or (len(row[0]) > 4):
                pass
            else:
                names.append(row[0])

    cols['Ticker Symbol'] = list()
    cols['Quarterly Revenue Growth'] = list()
    cols['Price Change (1 Year)'] = list()
    cols['Profit Margin'] = list()
    cols['Price/Sales'] = list()
    cols['Price/Earnings'] = list()
    cols['Price/Earnings Future'] = list()
    cols['Book Value/Share'] = list()
    cols['Market Cap'] = list()

    for n in names:
        try:

            url = 'https://finance.yahoo.com/quote/' + n + '/key-statistics?p=' + n
            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            QRG = soup.find(string='Quarterly Revenue Growth').parent.parent.next_sibling
            PS = soup.find(string='Price/Sales').parent.parent.next_sibling
            PE = soup.find(string='Trailing P/E').parent.parent.next_sibling
            PEF = soup.find(string ='Forward P/E').parent.parent.next_sibling
            BV = soup.find(string ='Book Value Per Share').parent.parent.next_sibling
            Profit = soup.find(string ='Profit Margin').parent.parent.next_sibling
            Change = soup.find(string = '52-Week Change').parent.parent.next_sibling
            MC = soup.find(string = 'Market Cap (intraday)').parent.parent.next_sibling

            x = cols.get('Ticker Symbol')
            x.append(n)
            x = cols.get('Quarterly Revenue Growth')
            x.append(QRG.text)
            x = cols.get('Price Change (1 Year)')
            x.append(Change.text)
            x = cols.get('Profit Margin')
            x.append(Profit.text)
            x = cols.get('Price/Sales')
            x.append(PS.text)
            x = cols.get('Price/Earnings')
            x.append(PE.text)
            x = cols.get('Price/Earnings Future')
            x.append(PEF.text)
            x = cols.get('Book Value/Share')
            x.append(BV.text)
            x = cols.get('Market Cap')
            x.append(MC.text)
        except:
                pass

    df = pd.DataFrame(cols, columns = ['Ticker Symbol', 'Quarterly Revenue Growth', 'Price Change (1 Year)', 'Profit Margin', 'Price/Sales', 'Price/Earnings', 'Price/Earnings Future', 'Book Value/Share', 'Market Cap'])
    out(df)

if __name__ == '__main__':
    main()





