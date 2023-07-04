from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

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
            item_data = {
                "item": cols[1].get_text(strip=True),
                "ge price": int(cols[2].get_text(strip=True).replace(',', '')),
                "high alch": int(cols[3].get_text(strip=True).replace(',', '')),
                "profit": int(cols[4].get_text(strip=True).replace(',', '')),
                "roi%": round(float(cols[5].get_text(strip=True).replace('%', ''))/100, 4),
                "limit": int(cols[6].get_text(strip=True).replace(',', '')),
                "volume": int(cols[7].get_text(strip=True).replace(',', '')),
                "max profit": int(cols[8].get_text(strip=True).replace(',', '')),
                "members": cols[9]['data-sort-value'].lower() == 'true', 
            }
            data.append(item_data)

    members = request.args.get('members')

    if members is not None:
        if members.lower() == 'true':
            data = [item for item in data if item['members'] is True]
        elif members.lower() == 'false':
            data = [item for item in data if item['members'] is False]
    
    data = sorted(data, key=lambda k: (k['volume'], k['max profit']), reverse=True)

    # Add order to data
    for i, item in enumerate(data, start=1):
        item['order'] = i

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))