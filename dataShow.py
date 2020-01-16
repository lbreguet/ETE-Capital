from urllib.request import urlopen
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

var_url = urlopen('https://www.predictit.org/api/marketdata/all')
xmldoc = parse(var_url, ET.XMLParser(encoding='utf-8'))

for market in xmldoc.iterfind('MarketList/Markets/MarketData'):
    name = market.findtext('Name')
    contracts = market.findtext('Contracts')

    print(name)
    print(contracts)
    print()
