import pdb
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

from market import Market
from agent import Trader
from utils import plot_2D


if __name__ == "__main__":
    # define 10 traders
    num_traders = 100
    timesteps = 1000
    # create a market
    market = Market(num_traders=num_traders)

    traders = []
    for i in range(num_traders):
        #init_balance = random.randint(2000, 10000)
        init_balance = 500
        init_shares = random.randint(5, 10)
        #init_shares = 5
        market.pre_distributed(init_shares)
        # determine trading strategy
        if random.random() > 1:
            trade_strat = "SMA"
            print(f"Agent {i} is using SMA")
        else:
            trade_strat = "Random"

        traders.append(Trader(init_balance=init_balance,
                              init_shares=init_shares,
                              trading_strategy=trade_strat))
    hist_price = []

    # Start the market
    market_done = False
    t = 0
    while not market_done:
        buy_list = []
        sell_list = []
        current_price = market.price
        hist_price.append(current_price)
        # each trader propose the quote
        for i in range(num_traders):
            s, b = traders[i].report_quote(current_price)
            sell_list.append(s)
            buy_list.append(b)
        # execute the transactions
        allocations = market.execute(buy_list, sell_list)

        # update traders' portfolio
        for i in range(num_traders):
            traders[i].update_portfolio(allocations[i], sell_list[i])
            assert (traders[i].balance >= 0)

        # check if the market is terminated
        t += 1
        if t >= timesteps:
            market_done = True

    # check the balance of different types of strategy
    sma_ = []
    random_ = []
    for i in range(num_traders):
        if traders[i].trading_strategy == "SMA":
            sma_.append(traders[i].balance)
        else:
            random_.append(traders[i].balance)

    if len(sma_) > 0:
        print(f"SMA average balance : {sum(sma_)/len(sma_)}")
    print(f"Random average balance : {sum(random_)/len(random_)}")
    plot_2D(np.arange(timesteps), hist_price, ["Price", "time steps", "price"])
