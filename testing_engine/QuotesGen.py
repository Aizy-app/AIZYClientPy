import pandas as pd
import random
import tkinter as tk
from tkinter import ttk
import mplfinance as mpf

import datetime as dt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import argparse

class QuotesGenerator:
    def __init__(self, length=50, min_close=1000, max_close=10000, up_candles_prob=0.5, max_candle_body=0.02, max_outlier=0.03,
                 minutes_per_candle=5, average_volatility=100):
        self.length = length
        self.min_close = min_close
        self.max_close = max_close
        self.up_candles_prob = up_candles_prob
        self.max_candle_body = max_candle_body
        self.max_outlier = max_outlier
        self.minutes_per_candle = minutes_per_candle
        self.average_volatility = average_volatility

    def generate_prices(self):
        prices = []
        open_price = random.uniform(self.min_close, self.max_close)
        current_time = dt.datetime.now()

        for _ in range(self.length):
            direction = "up" if random.random() <= self.up_candles_prob else "down"
            close_price = self.generate_close_price(open_price, direction)
            high_price, low_price = self.generate_high_low_prices(open_price, close_price)

            prices.append({
                "Timestamp": current_time,
                "Open": open_price,
                "High": high_price,
                "Low": low_price,
                "Close": close_price
            })

            current_time += dt.timedelta(minutes=self.minutes_per_candle)
            open_price = close_price
            self.prices = pd.DataFrame(prices)
        return pd.DataFrame(prices)

    def generate_close_price(self, open_price, direction):
        if direction == "up":
            max_possible_close = min(open_price + self.average_volatility, self.max_close)
            close_price = random.uniform(open_price, max_possible_close)
        else:
            min_possible_close = max(open_price - self.average_volatility, self.min_close)
            close_price = random.uniform(min_possible_close, open_price)

        return close_price

    def generate_high_low_prices(self, open_price, close_price):
        if random.random() <= self.max_outlier:
            high_price = max(open_price, close_price) + random.uniform(0, self.max_candle_body)
            low_price = min(open_price, close_price) - random.uniform(0, self.max_candle_body)
        else:
            body_range = abs(open_price - close_price) / 2
            high_price = max(open_price, close_price) + random.uniform(0, body_range)
            low_price = min(open_price, close_price) - random.uniform(0, body_range)

        return high_price, low_price


def plot_candlestick(df):
    fig, ax = mpf.plot(df, type='candle', style='charles', mav=(5, 10, 20), returnfig=True)
    return fig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Price Generator Script")
    parser.add_argument("--length", type=int, default=500, help="Length of the price generator")
    parser.add_argument("--min_close", type=int, default=1000, help="Minimum value for closing price")
    parser.add_argument("--max_close", type=int, default=15000, help="Maximum value for closing price")
    parser.add_argument("--minutes_per_candle", type=int, default=5, help="Minutes per candle")
    parser.add_argument("--up_candles_prob", type=float, default=0.5, help='Chances of generating an "up" candle')
    parser.add_argument("--max_candle_body", type=float, default=0.2, help="The maximum percentage of the candle body")
    parser.add_argument("--max_outlier", type=float, default=0.03, help='The probability of generating an "outlier"')
    args = parser.parse_args()
    my_gen = QuotesGenerator(args.length, args.min_close, args.max_close, args.up_candles_prob, args.max_candle_body)
    print(my_gen.generate_prices())
    