# Steam Market History Parser

This script allows you to parse your Steam Market transaction history and save it to a CSV file. The CSV file will contain the following columns:

- Name: The name of the item.
- Average Purchase Price: The average price at which you purchased the item.
- Quantity Purchased: The number of the item you purchased.
- Average Sale Price: The average price at which you sold the item.
- Quantity Sold: The number of the item you sold.
- Percentage Difference: The percentage difference between the purchase price and the sale price.
- Profit: The profit made from the transactions. It is calculated as the minimum of the quantity purchased and sold, multiplied by the difference between the average sale price and the average purchase price.

## Requirements

- Python 3.6 or higher

## Usage

1. Clone this repository.
2. Create a `data.py` file in the same directory as the script. This file should contain your cookies and headers for requests. You can get these from the Network tab in the developer console on the [Steam Market](https://steamcommunity.com/market/) page. Click on the "My market history" button, then copy the request as cURL (bash) and paste it into [this site](https://curlconverter.com/) to get the cookies and headers.
3. Run the script with the command `python main.py`.
4. The script will create a CSV file named `steam_history.csv` in the same directory.

## Notes

- The script includes a delay of 0.5 seconds between requests to avoid overwhelming the server.
- The script will make as many requests as necessary to retrieve the entire history.

## Disclaimer

This script is provided as is, without any guarantees. Use it responsibly and in accordance with Steam's terms of service.
