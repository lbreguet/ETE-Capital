import json
from openpyxl import *
from os import path
import pandas as pd
from pandas import json_normalize
import requests
import xlsxwriter




def get_markets():
    
    data = bytes_to_dict(read_xml('https://www.predictit.org/api/marketdata/all'))
   
    data = json.loads(data)
    markets = data['markets']  
    
    return markets


def read_xml(url):

    r = requests.get(url)

    content = r.content
    
 
    return content


def bytes_to_dict(data):

    return data.decode()


def to_xl():

    markets = get_markets()
    if (path.exists('markets.xlsx')):
        print('exists')
        workbook = load_workbook('markets.xlsx')
        writer = pd.ExcelWriter('markets.xlsx', engine='openpyxl')
        writer.book = workbook
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
        print(writer.book.worksheets[0].title)
        print(writer.book.worksheets[0].max_row)
        
        i = 0
        for market in markets:
        
            contracts = market['contracts']
            df = pd.DataFrame(contracts)
            del df['id']
            del df['name']
            del df['dateEnd']
            del df['image']
            del df['displayOrder']
            
            
            df.to_excel(writer, writer.book.worksheets[i].title, index=False, header=False, startrow=writer.book.worksheets[i].max_row)
            i += 1

        writer.close()
    else:
        print('doesnt exist')
        writer = pd.ExcelWriter('markets.xlsx')

        for market in markets:
        
            contracts = market['contracts']
            df = pd.DataFrame(contracts)
            del df['id']
            del df['name']
            del df['dateEnd']
            del df['image']
            del df['displayOrder']
            df.to_excel(writer, str(market['id']), index=False)

    
        writer.close()

        
    

    
    
          


to_xl()