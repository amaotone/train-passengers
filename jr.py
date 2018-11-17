import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def parse(url):
    resp = requests.get(url)
    bs = BeautifulSoup(resp.content, 'lxml')

    data = []
    for row in bs.select('table.passengerTable tr'):
        cells = list(row.find_all('td'))
        if len(cells) == 6:
            data.append({
                'Name': cells[1].text,
                'PassengerCount': int(cells[4].text.replace(',', ''))
            })
        elif len(cells) == 4:
            data.append({
                'Name': cells[0].text,
                'PassengerCount': int(cells[3].text.replace(',', ''))
            })
    return pd.DataFrame(data)


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    urls = ['http://www.jreast.co.jp/passenger/'] + [f'http://www.jreast.co.jp/passenger/2017_0{i}.html' for i in range(1, 10)]
    df = pd.concat([parse(url) for url in tqdm(urls)], ignore_index=True)
    df.to_csv('data/jr.csv')
