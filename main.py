import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd


def out(df):
    df.to_csv('output.csv')


def main():
    filename = "output.csv"

    cols = dict()

    names = list()

    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
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

            def findUncle(title):
                return soup.find(string = title).parent.parent.next_sibling

            def appendCol(name, val):
                x = cols.get(name);
                x.append(val);

            qrg = findUncle('Quarterly Revenue Growth')
            ps = findUncle('Price/Sales')
            pe = findUncle('Trailing P/E')
            pef = findUncle('Forward P/E')
            bv = findUncle('Book Value Per Share')
            profit = findUncle('Profit Margin')
            change = findUncle('52-Week Change')
            mc = findUncle('Market Cap (intraday)')

            appendCol('Ticker Symbol', n)
            appendCol('Quarterly Revenue Growth', qrg.text)
            appendCol('Price Change (1 Year)', change.text)
            appendCol('Profit Margin', profit.text)
            appendCol('Price/Sales', ps.text)
            appendCol('Price/Earnings', pe.text)
            appendCol('Price/Earnings Future', pef.text)
            appendCol('Book Value/Share', bv.text)
            appendCol('Market Cap', mc.text)

        except:
            pass
    df = pd.DataFrame(cols, columns=['Ticker Symbol', 'Quarterly Revenue Growth', 'Price Change (1 Year)', 'Profit Margin', 'Price/Sales', 'Price/Earnings', 'Price/Earnings Future', 'Book Value/Share', 'Market Cap'])
    out(df)


if __name__ == '__main__':
    main()
