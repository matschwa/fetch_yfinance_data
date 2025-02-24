"""
Script to download historical stock price data from Yahoo Finance


Sources if inspiration: 
    https://www.youtube.com/watch?v=WosSGiBmMHs
    https://www.capstonetradingsystems.com/post/python-script-to-download-10-year-of-historical-data-on-500-companies-in-yahoo-finance

"""
#%%
import yfinance as yf
import os
import pandas as pd
import pickle
import json
from tqdm import tqdm
from ratelimit import limits, sleep_and_retry

#%%
ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 120  # Adjust if needed

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def get_ticker_data(ticker):
    data = yf.download(ticker,  period="2y", interval="1d", multi_level_index=False, 
                       threads=False, progress=False)
    return data

#%%

def main():
    
    ### get dict of stocks from file
    with open("gettex_filtered_tickers.txt", "r") as f: 
        tkrs_all = f.read().split("\n")

    data_all = {}

    for ticker in tqdm(tkrs_all, desc="Processing tickers"):
        data_all[ticker] =  get_ticker_data(ticker)

    # Save data to text file
    output_file = os.path.join("downloads/price_data_all.pkl")
    with open(output_file, 'wb') as f:
        pickle.dump(data_all, f, protocol=pickle.HIGHEST_PROTOCOL)

#%%
if __name__ == "__main__":
    # Create downloads folder if it doesn't exist
    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    main()

# %%
