import pandas as pd
import requests
from dash import Dash, html
import math


response = requests.get('https://poe.ninja/api/data/itemoverview?league=Affliction&type=Essence')

if response.status_code == 200:
    # Process the response content here
    data = response.json()
else:
    print(f"Request failed with status code: {response.status_code}")
df = pd.json_normalize(data, 'lines')
screamingDF = df.loc[df.name.str.contains('Screaming')]
shriekingDF = df.loc[df.name.str.contains('Shrieking')]
deafeningDF = df.loc[df.name.str.contains('Deafening')]
types = ['Greed', 'Contempt', 'Hatred', 'Woe', 'Fear', 'Anger', 'Torment', 'Sorrow', 'Rage', 'Suffering', 'Wrath', 'Doubt', 'Loathing',
         'Zeal', 'Anguish', 'Spite', 'Scorn', 'Envy', 'Misery', 'Dread']
prices = {}
upgrade = {}
essences = [shriekingDF, deafeningDF]
for type in types:
    temp = []
    for essence in essences:
        essenceValue = essence[essence.name.str.contains(type)]['chaosValue'].values[0]
        temp.append(essenceValue)
    prices[type] = temp
print(prices)
for key in prices:
    if math.floor(prices[key][1]) > 3 * prices[key][0]:
        upgrade[key] = "YES"
    else: 
        upgrade[key] = "no"


app = Dash(__name__)

server = app.server

half = len(upgrade) // 2 + 2
leftSide = dict(list(upgrade.items())[:half])
rightSide = dict(list(upgrade.items())[half:])
leftPrice = dict(list(prices.items())[:half])
rightPrice = dict(list(prices.items())[half:])
app.layout = html.Div([
    html.Table([
        html.Tr([html.Th("Key"), html.Th("Upgrade"), html.Th("Shrieking"), html.Th("Deafening")]),
        *[
            html.Tr([html.Td(key), html.Td(str(value)), html.Td(leftPrice[price][0]), html.Td(str(leftPrice[price][1]))])
            for key, value, price in zip(leftSide.keys(), leftSide.values(), leftPrice)
        ]
    ], style={'display': 'inline-block', 'width': '20%', 'vertical-align': 'top'}),

    html.Table([
        html.Tr([html.Th("Key"), html.Th("Upgrade"), html.Th("Shrieking"), html.Th("Deafening")]),
        *[
            html.Tr([html.Td(key), html.Td(str(value)), html.Td(rightPrice[price][0]), html.Td(str(rightPrice[price][1]))])
            for key, value, price in zip(rightSide.keys(), rightSide.values(), rightPrice)
        ]
    ], style={'display': 'inline-block', 'width': '20%', 'vertical-align': 'top'}),
], style={'text-align': 'center'})

# Run server
if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)