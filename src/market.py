import pdb
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple


class Market(object):
    """
    A simple market that simulate the stock price based on supply and demand
    from traders
    """
    def __init__(self, initial_total_shares=100, initial_price=15,
                 num_traders=3, name="Chan-Wei company"):
        # Initial released shares by current company
        self.initial_total_shares = initial_total_shares
        self.price = initial_price
        self.num_traders = num_traders
        self.name = name

        # time step initialization
        self.timestep = 0

        # keep track of the remaining stocks available in the market
        self.shares_in_market = initial_total_shares

        # print the information
        print(f"================= [{self.name}] ====================")
        print(f"Initial shares released : {self.initial_total_shares}")
        print(f"Initial price           : {self.price}")
        print(f"Number of traders       : {self.num_traders}")
        print(f"====================== [Done] ===========================\n")

    def _determine_price_(self, total_buy: int, total_sell: int,
                          total_supply: int):
        # use my current naive equation to determine the price
        # new price
        self.price = self.price * (1 + (total_buy - total_sell) / total_supply)

        # update the number of shares available in the market
        self.shares_in_market += total_sell - total_buy

    def _satisfy_demand_(self, buy_list: np.array, avail_shares: int):
        # allocate shares based on the number of available shares
        share_allocation = np.zeros(self.num_traders)
        trader_ids = np.arange(self.num_traders)
        _avail_shares = avail_shares

        while True:
            # pick one trader and allocate a share for him
            trader_id = np.random.choice(trader_ids, 1)[0]
            share_allocation[trader_id] += 1
            _avail_shares -= 1
            # if he is satisfied, remove him from list
            if share_allocation[trader_id] == buy_list[trader_id]:
                trader_ids = np.delete(trader_ids,
                                       np.where(trader_ids == trader_id))
            # if all available shares are given, terminate
            if _avail_shares == 0:
                break
        return share_allocation

    def execute(self, buy_list: np.array, sell_list: np.array):
        # sell will always be execute...
        total_buy = np.sum(buy_list)
        total_sell = np.sum(sell_list)
        total_supply = total_sell + self.shares_in_market

        # == check if everything satisfies the constraints ===
        # when demand is larger than the supply, randomly assign the shares to
        # traders
        if total_buy > total_supply:
            # total_buy is more than total_supply
            total_buy = total_supply
        assert (total_supply <= self.initial_total_shares)
        # ====================================================

        # assign the shares
        share_allocation = self._satisfy_demand_(buy_list, total_buy)

        # determine price for next step
        print(f"Old price : {self.price}")
        self._determine_price_(total_buy, total_sell, total_supply)
        print(f"New price : {self.price}")
        print(f"Number of shares available in the market: {self.shares_in_market}")

        return share_allocation

# Test code
if __name__ == "__main__":
    # create a market
    market = Market()

    # traders buy list and sell list
    b = np.array([10, 5, 6])
    s = np.array([0, 0, 0])
    print(f"Buy  : {b}, Total buy : {np.sum(b)}")
    print(f"Sell : {s}, Total sell: {np.sum(s)}")
    market.execute(b, s)
    print("-------------------------------------")

    b = np.array([0, 2, 0])
    s = np.array([3, 0, 4])
    print(f"Buy  : {b}, Total buy : {np.sum(b)}")
    print(f"Sell : {s}, Total sell: {np.sum(s)}")
    market.execute(b, s)
    print("-------------------------------------")

    b = np.array([50, 10, 0])
    s = np.array([0, 0, 2])
    print(f"Buy  : {b}, Total buy : {np.sum(b)}")
    print(f"Sell : {s}, Total sell: {np.sum(s)}")
    market.execute(b, s)
    print("-------------------------------------")


