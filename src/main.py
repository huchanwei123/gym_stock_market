import pdb
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple

from market import Market
from agent import Trader
from utils import plot_2D, plot_2Ds, plot_bar


if __name__ == "__main__":
    # define 10 traders
    num_traders = 100
    timesteps = 2000
    # create a market
    market = Market(num_traders=num_traders)

    traders = []
    random.seed(20)
    for i in range(num_traders):
        #init_balance = random.randint(500, 1000)
        init_balance = 500
        #init_shares = random.randint(20, 40)
        init_shares = 20
        market.pre_distributed(init_shares)
        # determine trading strategy
        #if random.random() > 0.9:
        if i < 1:
            trade_strat = "SMA"
            #init_balance = 750
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
    sma_balance = []
    random_balance = []
    sell_buy_diff = []
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
        sell_buy_diff.append(sum(buy_list) - sum(sell_list))

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
                #sma_.append(traders[i].balance)
                sma_.append(traders[i].hist_total_balance[-1])
            else:
                #random_.append(traders[i].balance)
                random_.append(traders[i].hist_total_balance[-1])

        if len(sma_) > 0:
            sma_balance.append(sum(sma_)/len(sma_))
        random_balance.append(sum(random_)/len(random_))

    # extract the action history from SMA agents
    sma_action_hist = traders[0].hist_action
    sma_shares_hold_hist = traders[0].hist_shares_hold

    if len(sma_balance) > 0:
        print(f"Number of SMA agents: {len(sma_)}")
        print(f"Final SMA average balance : {sma_balance[-1]}")
    print(f"Final random average balance : {random_balance[-1]}")
    plot_2D(np.arange(timesteps), hist_price, [f"Price", "time steps", "price"])
    plot_2D(np.arange(timesteps), sell_buy_diff, [f"Difference between sell and buy", "time steps", "difference"])
    plot_bar(np.arange(timesteps), sma_action_hist,
            [f"SMA hisorical actions", "time steps", "action taken"])
    plot_bar(np.arange(timesteps), sma_shares_hold_hist,
            [f"SMA hisorical shares held", "time steps", "shares"])
    plot_2Ds(np.arange(timesteps), [sma_balance, random_balance],
            ["Balance Comparison", "time steps", "balance"],
            ["SMA", "Random"])
    pdb.set_trace()