import getopt
import json
import requests
import sys


def getMarkets():
    
    data = bytesToDict(readXML('https://www.predictit.org/api/marketdata/all'))
    data = json.loads(data)

    return data['markets']

def readXML(URL):

    r = requests.get(URL)
    content = r.content

    return content


def bytesToDict(data):
    return data.decode()

def printData(args):

    search = getopt.getopt(args, ':')
    searchString = ""
    searchString = searchString.join(search[1])

    markets = getMarkets()


    for market in markets:
        
        contracts = market['contracts']

        if (len(contracts) >= 2):
            
            if searchString in market['name']:

                name = market['name']
                status = market['status']

                print(name)
                print(status)
                print('Contracts:')
                for contract in contracts:
                    cname = contract['name']
                    cstatus = contract['status']
                    last_trade_price = contract['lastTradePrice']
                    best_buy_yes_cost = contract['bestBuyYesCost']
                    best_buy_no_cost = contract['bestBuyNoCost']
                    best_sell_yes_cost = contract['bestSellYesCost']
                    best_sell_no_cost = contract['bestSellNoCost']
                    last_close_price = contract['lastClosePrice']

                    print(cname)
                    print(cstatus)
                    print("Last Trade Price: " + str(last_trade_price))
                    print("Best Buy Yes Cost: " + str(best_buy_yes_cost))
                    print("Best Buy No Cost: " + str(best_buy_no_cost))
                    print("Best Sell Yes Cost: " + str(best_sell_yes_cost))
                    print("Best Sell No Cost: " + str(best_sell_no_cost))
                    print("Last Close Price: " + str(last_close_price))
                
                    print()
            
            
                print('----------------------------------')

printData(sys.argv[1:])