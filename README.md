DW Alcher's Microservice
GEAlcher is a Flask-based microservice that retrieves the most profitable items for high alchemy from the RuneScape's Grand Exchange. It accomplishes this by scraping the Alchemy page on the Old School RuneScape Wiki and sorting the items based on the maximum possible profit and trading volume.

Key Features:

* Web Scraping: Using Python's BeautifulSoup library, the microservice scrapes the Alchemy page of the Old School RuneScape Wiki, fetching data for each item including its GE price, High Alchemy value, profit, return on investment (ROI), limit, trading volume, whether it is members only, and the maximum possible profit.

* Item ID Fetching: To make its data more useful, the microservice also fetches the unique item ID for each item. It achieves this by loading item data from a JSON file hosted on GitHub and comparing the item names.

* Data Filtering: Through a GET parameter, the microservice allows clients to filter the returned data based on whether the items are members-only or not.

* Data Sorting: The scraped data is sorted based on trading volume and maximum possible profit, making it easy to identify the most profitable items quickly.

* Data Serving: The microservice serves the collected and processed data as JSON via a Flask route, making it easily accessible for the Alcher bot or any other application.

* Environmentally Aware: The service retrieves its running port from an environment variable, making it adaptable to different hosting environments.

GEAlcher stands as an intermediary between the Alcher bot and the Old School RuneScape Wiki, taking care of the heavy lifting of data collection and processing. It fetches, parses, sorts, and serves the data needed by the bot, making it an integral part of the bot's intelligent item selection feature. This greatly enhances the bot's capabilities, contributing to making RuneScape's High Alchemy an automated, profitable endeavor.
