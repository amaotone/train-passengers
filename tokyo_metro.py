import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

os.makedirs('data', exist_ok=True)
resp = requests.get('https://www.tokyometro.jp/corporate/enterprise/passenger_rail/transportation/passengers/index.html')
bs = BeautifulSoup(resp.content, 'lxml')

data = []
for row in bs.select('table.dataTable tr'):
    cells = list(row.find_all('td'))
    if len(cells) == 5:
        data.append({
            'Name': cells[2].text,
            'PassengerCount': int(cells[3].text.replace(',', '')),
            'RouteCount': len(cells[1].find_all('img'))
        })
    if len(cells) == 4:
        data.append({
            'Name': cells[1].text,
            'PassengerCount': int(cells[2].text.replace(',', '')),
            'RouteCount': len(cells[0].find_all('img'))
        })

df = pd.DataFrame(data)
df = df.groupby('Name').sum().reset_index()
names = df.Name.apply(lambda x: pd.Series(re.split('[〈・]', x.replace('〉', ''))))
names.columns = ['Name', 'Name2']
pd.concat([names, df.drop('Name', axis=1)], axis=1).to_csv('data/tokyo_metro.csv')
