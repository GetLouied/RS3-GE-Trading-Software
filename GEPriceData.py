import pandas as pd
import requests

url = "https://runescape.wiki/?title=Module:GEPrices/data.json&action=raw&ctype=application%2Fjson"
r = requests.get(url)
data = r.json()

keys, values = zip(*data.items())

GEPrices = pd.DataFrame({'Item': keys, 'Price': values})
print(GEPrices)
