import json
import openpyxl
import pandas as pd
from pandas import json_normalize
import requests




def get_markets():
    
    data = bytes_to_dict(read_xml('https://www.predictit.org/api/marketdata/all'))
   
    data = json.loads(data)
    data = data['markets']
    
    df = pd.DataFrame(data)
    df.to_excel('markets.xlsx')
    return df

def read_xml(url):

    r = requests.get(url)

    content = r.content
    
 
    return content


def bytes_to_dict(data):

    return data.decode()


get_markets()