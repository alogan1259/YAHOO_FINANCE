#scrape.py
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


def get_most_active():
    url = 'https://finance.yahoo.com/trending-tickers'
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    ticker_data = {}
    r = requests.get(url, headers=headers)
    data = r.text 
    soup = BeautifulSoup (data, 'html.parser')
    alldata = soup.find_all('tr', class_='simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)')
    table1 = alldata[0]
    for cols in alldata:
        t = cols.find_all('td')
        cells = cols.find_all('fin-streamer')
        if cells:
            ticker = t[0].text
            name = t[1].text
            value = t[2].text
            time = t[3].text
            change = t[4].text
            percent_change = t[5].text
            volume = t[6].text
            market_cap = t[7].text
            ticker_data[ticker] = {
                'name': name,
                'value': value,
                'time': time,
                'change': change,
                'percent_change': percent_change,
                'volume': volume,
                'market_cap': market_cap,
            }
    return ticker_data


def create_df():
    ticker_data = get_most_active()
    stock_data = []
    for ticker, data in ticker_data.items():
        value = get_value(data)
        timestamp = pd.Timestamp.now()
        stock_data.append({
            'timestamp': timestamp,
            'ticker': ticker,
            'name': data['name'],
            'value': value,
            'time': data['time'],
            'change': data['change'],
            'percent_change': data['percent_change'],
            'volume': data['volume'],
            'market_cap': data['market_cap']
        })
    df = pd.DataFrame(stock_data)
    return df


def get_all_names():
    ticker_data = get_most_active()
    ticker_names = []
    for ticker, data in ticker_data.items():
        ticker_names.append(data['name'])
    return ticker_names


def get_biggest_movers():
    ticker_data = get_most_active()
    # Sort the ticker data by absolute value of percent change
    sorted_ticker_data = sorted(ticker_data.items(), key=lambda x: abs(float(x[1]['percent_change'][:-1])), reverse=True)
    biggest_movers = []
    for ticker, data in sorted_ticker_data[:5]:
        biggest_movers.append((ticker, data['percent_change']))
    return biggest_movers


def get_name(ticker_name):
    return ticker_name['name']


def get_value(ticker_name):
    return ticker_name['value']


def get_time(ticker_name):
    return ticker_name['time']


def get_change(ticker_name):
    return ticker_name['change']


def get_percent_change(ticker_name):
    return ticker_name['percent_change']


def get_volume(ticker_name):
    return ticker_name['volume']


def get_market_cap(ticker_name):
    return ticker_name['market_cap']
