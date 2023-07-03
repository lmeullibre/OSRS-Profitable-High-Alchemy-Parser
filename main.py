from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def scrape_website():
    url = "https://oldschool.runescape.wiki/w/RuneScape:Grand_Exchange_Market_Watch/Alchemy"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.select_one('.wikitable.sortable.sticky-header')

    # Get the header
    header = [col.get_text(strip=True) for col in table.find_all('th')]

    # Find all rows in the table
    rows = table.find_all('tr')[1:]  # Skip the header row

    # This will store the row data
    data = []

    # Loop over the rows
    for i, row in enumerate(rows):
        # Find all columns in the row, excluding the first (icon) column
        cols = row.find_all('td')[1:]
        
        # Get the text inside each <td>
        cols = [col.get_text(strip=True) if col.get_text(strip=True) else 'N/A' for col in cols]

        # If there are not enough columns, fill in the missing ones with 'N/A'
        if len(cols) < len(header):
            cols.extend(['N/A'] * (len(header) - len(cols)))

        # Check the "members" column and replace its value based on the "data-sort-value" attribute
        for j, col in enumerate(row.find_all('td')[1:]):
            if header[j] == "Members":
                cols[j] = True if col['data-sort-value'] == 'true' else False
            elif header[j] == "ROI%":
                if cols[j] != 'N/A':
                    # Convert the string to a float, divide it by 100, and round to 3 decimal places
                    cols[j] = round(float(cols[j].replace('%', '')) / 100, 3)
            else:
                # Convert the other columns to integer if possible
                if cols[j] != 'N/A':
                    try:
                        cols[j] = int(cols[j].replace(',', ''))
                    except ValueError:
                        cols[j] = None  # Or set another appropriate default value

        # Create a dictionary for this row
        row_dict = dict(zip(header, cols))

        # Add the row's dictionary to our data array
        data.append(row_dict)

    return jsonify({"data": data})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))