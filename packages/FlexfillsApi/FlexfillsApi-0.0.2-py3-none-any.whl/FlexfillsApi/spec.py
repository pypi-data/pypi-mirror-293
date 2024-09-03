import os
from flexfillsapi import initialize

# creds to test enviroment 100000_german, password abc123

username = '100000_german'
password = 'abc123'

instruments = ["ETH/BTC", "BTC/USD", "BTC/EUR"]
currencies = ["USD", "ETH"]
statues = ["COMLETED", "REJECTED", "PARTIALLY_FILLED", "FILLED", "EXPIRED"]

date_from = "2022-12-01T00:00:00"
date_to = "2022-12-14T22:30:00"


def get_order_books_stream(resp):
    print(resp)

def main():
    flexfills = initialize(username, password, is_test=True)
    # resp = flexfills.get_balance(["USD", "ETH"])

    # resp = flexfills.get_order_history(date_from, date_to, instruments, statues)
    resp = flexfills.subscribe_order_books(["BTC/USDT"])
    # resp = flexfills.get_trade_positions()

    print(resp)


if __name__ == "__main__":
    main()
