import requests
import csv
import time
from collections import defaultdict
from data import cookies, headers

def get_history(count, start):
    params = [
        ('count', str(count)),
        ('start', str(start)),
        ('norender', '1'),
    ]
    response = requests.get('https://steamcommunity.com/market/myhistory', params=params, cookies=cookies, headers=headers)
    return response.json()

def parse_history(history, purchases, sales):
    if 'events' not in history:
        print("No events found")
        return
    for event in history['events']:
        listing_id = event['listingid']
        event_type = event['event_type']

        if 'purchaseid' not in event:
            continue

        purchase_id = event['purchaseid']

        asset = history['listings'][listing_id]['asset']
        appid = asset['appid']
        contextid = asset['contextid']
        asset_id = asset['id']

        name = history['assets'][str(appid)][str(contextid)][asset_id]['name']

        if event_type == 3:  # Sale
            amount = history['purchases'][f"{listing_id}_{purchase_id}"]['received_amount'] / 100
            sales[name].append(amount)
        elif event_type == 4:  # Purchase
            amount = (history['purchases'][f"{listing_id}_{purchase_id}"]['paid_amount'] + history['purchases'][f"{listing_id}_{purchase_id}"]['paid_fee']) / 100
            purchases[name].append(amount)

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Average Purchase Price", "Quantity Purchased", "Average Sale Price", "Quantity Sold", "Percentage Difference", "Profit"])
        writer.writerows(data)

def main():
    start = 0
    count = 500
    total_count = count
    purchases = defaultdict(list)
    sales = defaultdict(list)

    while start < total_count:
        history = get_history(count, start)
        total_count = history['total_count']
        parse_history(history, purchases, sales)
        print(f"Processed: {start}, Remaining: {total_count - start}")
        start += count
        time.sleep(1)  # Add delay

    parsed_data = []
    for name in set(list(sales.keys()) + list(purchases.keys())):
        avg_purchase_price = sum(purchases[name]) / len(purchases[name]) if purchases[name] else 0
        quantity_purchased = len(purchases[name])
        avg_sale_price = sum(sales[name]) / len(sales[name]) if sales[name] else 0
        quantity_sold = len(sales[name])
        percentage_difference = ((avg_sale_price - avg_purchase_price) / avg_purchase_price) * 100 if avg_purchase_price else 0
        profit = min(quantity_purchased, quantity_sold) * (avg_sale_price - avg_purchase_price)
        parsed_data.append([name, avg_purchase_price, quantity_purchased, avg_sale_price, quantity_sold, percentage_difference, profit])

    save_to_csv(parsed_data, 'steam_history.csv')

if __name__ == "__main__":
    main()
