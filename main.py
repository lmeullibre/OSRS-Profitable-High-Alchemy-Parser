from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import os
import json

app = Flask(__name__)

# Load item data from JSON file
item_data_url = "https://raw.githubusercontent.com/0xNeffarion/osrsreboxed-db/master/data/items/items-cache-data.json"
response = requests.get(item_data_url)
item_data_dict = json.loads(response.text)

@app.route('/', methods=['GET'])
def scrape_data():
    url = "https://oldschool.runescape.wiki/w/RuneScape:Grand_Exchange_Market_Watch/Alchemy"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select_one('.wikitable.sortable.sticky-header')

    data = []
    rows = table.select('tbody > tr')
    for row in rows:
        cols = row.select('td')

        if len(cols) >= 10:
            item_name = cols[1].get_text(strip=True)
            item_id = get_item_id(item_name)
            item_data = {
                "id": item_id,
                "item": item_name,
                "ge_price": int(cols[2].get_text(strip=True).replace(',', '')),
                "high_alch": int(cols[3].get_text(strip=True).replace(',', '')),
                "profit": int(cols[4].get_text(strip=True).replace(',', '')),
                "roi": round(float(cols[5].get_text(strip=True).replace('%', ''))/100, 4),
                "limit": int(cols[6].get_text(strip=True).replace(',', '')),
                "volume": int(cols[7].get_text(strip=True).replace(',', '')),
                "max_profit": int(cols[8].get_text(strip=True).replace(',', '')),
                "members": cols[9]['data-sort-value'].lower() == 'true',
            }
            data.append(item_data)

    nature_rune_url = "https://oldschool.runescape.wiki/w/Nature_rune"
    response = requests.get(nature_rune_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    nature_rune_price = int(soup.select_one('.infobox-quantity').get_text(strip=True).split()[0].replace('coins', ''))

    item_data = {
        "id": get_item_id("Nature rune"),
        "item": "Nature rune",
        "ge_price": nature_rune_price,
        "high_alch": 0,  
        "profit": 0,      
        "roi": 0.0,       
        "limit": 0,       
        "volume": 0,      
        "max_profit": 0,  
        "members": False,
    }
    data.append(item_data)        

    members = request.args.get('members')

    if members is not None:
        if members.lower() == 'true':
            data = [item for item in data if item['members'] is True]
        elif members.lower() == 'false':
            data = [item for item in data if item['members'] is False]

    data = sorted(data, key=lambda k: (k['volume'], k['max_profit']), reverse=True)

    # Add order to data
    for i, item in enumerate(data, start=1):
        item['order'] = i

    return jsonify(data)


def get_item_id(item_name):
    for item_id, item_data in item_data_dict.items():
        if item_data['name'].lower() == item_name.lower():
            return int(item_id)
    return None


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))