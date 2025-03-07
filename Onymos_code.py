import random
import time
import threading

MAX_TICKERS = 1024
buy_orders = [[] for _ in range(MAX_TICKERS)]  
sell_orders = [[] for _ in range(MAX_TICKERS)]  


def get_ticker_index(ticker):
    return sum(ord(c) for c in ticker) % MAX_TICKERS


def match_orders(ticker_index):
    i, j = 0, 0
    while i < len(buy_orders[ticker_index]) and j < len(sell_orders[ticker_index]):
        buy_order = buy_orders[ticker_index][i]
        sell_order = sell_orders[ticker_index][j]

        if buy_order[2] >= sell_order[2]:  # Match found
            executed_quantity = min(buy_order[1], sell_order[1])
            print(f"Trade Executed: {executed_quantity} shares at ${sell_order[2]} for ticker {buy_order[0]}")

            buy_order[1] -= executed_quantity
            sell_order[1] -= executed_quantity

            if buy_order[1] == 0:
                i += 1
            if sell_order[1] == 0:
                j += 1
        else:
            break  # No match found

    buy_orders[ticker_index] = buy_orders[ticker_index][i:]
    sell_orders[ticker_index] = sell_orders[ticker_index][j:]


def add_order(order_type, ticker, quantity, price):
    ticker_index = get_ticker_index(ticker)
    timestamp = time.time()
    order = [ticker, quantity, price, timestamp]

    if order_type == "Buy":
        buy_orders[ticker_index].append(order)
    else:
        sell_orders[ticker_index].append(order)

    match_orders(ticker_index)


def simulate_orders(num_orders=100):
    tickers = ["AAPL", "GOOG", "MSFT", "TSLA", "AMZN", "NFLX", "NVDA", "META"]

    for _ in range(num_orders):
        order_type = "Buy" if random.randint(0, 1) == 0 else "Sell"
        ticker = tickers[random.randint(0, len(tickers) - 1)]
        quantity = random.randint(1, 100)
        price = round(random.uniform(100, 1000), 2)

        threading.Thread(target=add_order, args=(order_type, ticker, quantity, price)).start()
        time.sleep(random.uniform(0.1, 0.5))


if __name__ == "__main__":
    simulate_orders(50)
