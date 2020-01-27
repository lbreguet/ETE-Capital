import os
import xml.etree.ElementTree as ET
import requests

URL = 'https://www.predictit.org/api/marketdata/all'

r = requests.get(URL)
with open('data/data.xml', 'wb') as f:
    f.write(r.content)

file_name = 'data.xml'
full_file = os.path.abspath(os.path.join('data', file_name))

print(full_file)

dom = ET.parse(full_file)

markets = dom.findall('Markets/MarketData')

print('Markets:')

for market in markets:
 
    contracts = market.findall('Contracts/MarketContract')

    if (len(contracts) >= 2):
        name = market.find('Name')
        status = market.find('Status')
        print(name.text)
        print(status.text)
        print('Contracts:')

        for contract in contracts:
            cname = contract.find('Name')
            cstatus = contract.find('Status')
            last_trade_price = contract.find('LastTradePrice')
            best_buy_yes_cost = contract.find('BestBuyYesCost')
            best_buy_no_cost = contract.find('BestBuyNoCost')
            best_sell_yes_cost = contract.find('BestSellYesCost')
            best_sell_no_cost = contract.find('BestSellNoCost')
            last_close_price = contract.find('LastClosePrice')

            print(cname.text)
            print(cstatus.text)
            print("Last Trade Price: " + str(last_trade_price.text))
            print("Best Buy Yes Cost: " + str(best_buy_yes_cost.text))
            print("Best Buy No Cost: " + str(best_buy_no_cost.text))
            print("Best Sell Yes Cost: " + str(best_sell_yes_cost.text))
            print("Best Sell No Cost: " + str(best_sell_no_cost.text))
            print("Last Close Price: " + str(last_close_price.text))
            print()

        print()
        print()



