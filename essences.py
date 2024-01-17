import pandas as pd
import requests
from dash import Dash, html
import math


response = requests.get('https://poe.ninja/api/data/itemoverview?league=Affliction&type=Essence')
data = response.json()
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
app.layout = html.Div([
    html.Table([
        html.Tr([html.Th("Key"), html.Th("Upgrade")]),
        *[
            html.Tr([html.Td(key), html.Td(str(value))])
            for key, value in leftSide.items()
        ]
    ], style={'display': 'inline-block', 'margin': 'auto', 'width': '20%', 'vertical-align': 'top'}),

    html.Table([
        html.Tr([html.Th("Key"), html.Th("Upgrade")]),
        *[
            html.Tr([html.Td(key), html.Td(str(value))])
            for key, value in rightSide.items()
        ]
    ], style={'display': 'inline-block', 'margin': 'auto', 'width': '20%', 'vertical-align': 'top'})
], style={'text-align': 'center'})

# Run server
if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)