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
        
        # Ensure the row has enough columns
        if len(cols) >= 10:
            item_data = {
                "Item": cols[1].get_text(strip=True),
                "GE Price": int(cols[2].get_text(strip=True).replace(',', '')),
                "High Alch": int(cols[3].get_text(strip=True).replace(',', '')),
                "Profit": int(cols[4].get_text(strip=True).replace(',', '')),
                "ROI%": round(float(cols[5].get_text(strip=True).replace('%', ''))/100, 4),
                "Limit": int(cols[6].get_text(strip=True).replace(',', '')),
                "Volume": int(cols[7].get_text(strip=True).replace(',', '')),
                "Max profit": int(cols[8].get_text(strip=True).replace(',', '')),
                "Members": cols[9]['data-sort-value'].lower() == 'true',  # Convert string to boolean
            }
            data.append(item_data)

    members = request.args.get('members')

    if members is not None:
        if members.lower() == 'true':
            data = [item for item in data if item['Members'] is True]
        elif members.lower() == 'false':
            data = [item for item in data if item['Members'] is False]
    
    data = sorted(data, key=lambda k: (k['Volume'], k['Max profit']), reverse=True)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))