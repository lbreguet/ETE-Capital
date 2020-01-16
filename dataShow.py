import urllib
import xmltodict

file = urllib.request.urlopen('https://www.predictit.org/api/marketdata/all')
data = file.read()
file.close()

data = xmltodict.parse(data)
data