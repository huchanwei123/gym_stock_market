import pdb
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

class Trader(object):
    def __init__(self, init_balance, init_shares, trading_strategy="Random"):
        self.balance = init_balance

        # record the historical prices
        self.hist_price = []

        # action set definition...
        # only one share is performed each time
        self.action_set = {0: "sell",
                           1: "buy",
                           2: "do nothing"}
        self.trading_strategy = trading_strategy
        self.shares_hold = init_shares
        # keep track of action history
        self.hist_action = []
        self.hist_balance = [init_balance]
        self.hist_shares_hold = []
        self.hist_total_balance = []

    def _trading_strategy_(self, signal=None):
        # define the trading strategy here...
        # currently support random, SMA
        current_price = self.hist_price[-1]
        if self.trading_strategy == "Random":
            action = random.randint(0, len(self.action_set)-1)
        if self.trading_strategy == "SMA":
            short_horizon = 10
            long_horizon = 50
            short_hist = self.hist_price[-short_horizon:]
            long_hist = self.hist_price[-long_horizon:]
            ma_short = sum(short_hist) / len(short_hist)
            ma_long = sum(long_hist) / len(long_hist)
            # simple rule
            if ma_short > ma_long:
                # buy
                action = 1
            #if ma_price >= current_price:
            #    action = 0
            else:
                action = 0
        # check if the shares or balance are enough...
        if action == 0 and self.shares_hold <= 0:
            action = 2
        if action == 1 and self.balance <= 0:
            action = 2

        self.hist_action.append(action)
        return action

    def report_quote(self, current_price):
        # based on the selected action, just report it for one share
        sell_amount = 0
        buy_amount = 0
        self.hist_price.append(current_price)
        action = self._trading_strategy_()
        if self.action_set[action] == "sell" and self.shares_hold > 0:
            sell_amount = 1
        if self.action_set[action] == "buy" and self.balance > current_price:
            buy_amount = 1
        return sell_amount, buy_amount

    def update_portfolio(self, actual_buy, actual_sell):
        # For now, we always allow to sell but maybe not allow to buy
        # It depends on how many shares available...
        # update the portfolio
        current_price = self.hist_price[-1]
        self.shares_hold += actual_buy - actual_sell
        self.balance += current_price * (actual_sell - actual_buy)

        # record the balance
        self.hist_balance.append(self.balance)
        self.hist_shares_hold.append(self.shares_hold)
        self.hist_total_balance.append(current_price * self.shares_hold + self.balance)
