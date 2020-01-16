from xml.etree.ElementTree import parse
from urllib.request import urlopen
from lxml import etree

var_url = urlopen('https://www.predictit.org/api/marketdata/all')
parser = etree.XMLParser(recover=True)
xmldoc = parse(var_url, parser=parser)
print(var_url)
print(xmldoc)