"""
Fetch all financial data from Yahoo Finance.


"""
#%% Imports
import yfinance as yf
import os
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm
import pickle

#%% G dict of stocks from file
with open("gettex_filtered_tickers.txt", "r") as f: 
    tkrs_all = f.read().split("\n")
    
SYMBOLS = tkrs_all


#%% Define functions

def fetch_all_basis_data(ticker):
    """Fetch all necessary financial statements once and return as a dictionary."""
    try:
        return {
            "income_stmt": fetch_data(ticker,"income_stmt"),
            "balance_sheet": fetch_data(ticker, "balance_sheet"),
            "cash_flow": fetch_data(ticker, "cash_flow"),
            "info":fetch_data(ticker, "info"),
            "basis_data":fetch_data(ticker, "basis_data")
        }
    except Exception as e:
        print(f"Error fetching basis_data for {ticker}: {e}")
        return None

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 200  # Adjust if needed

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def fetch_data(ticker, data_type):
    """
    Fetch a specific financial statement while respecting rate limits.
    
    :param ticker: yfinance.Ticker object
    :param data_type: str, one of ["income_stmt", "balance_sheet", "cash_flow", "info", "basis_data"]
    :return: Requested financial data
    """
    data_map = {
        "income_stmt": ticker.income_stmt,
        "balance_sheet": ticker.balance_sheet,
        "cash_flow": ticker.cash_flow,
        "info": ticker.info,
        "financials": ticker.financials
    }
    
    return data_map.get(data_type, f"Invalid data type: {data_type}")


def main():
    """Main function to fetch financial data for all symbols."""
    # Initialize an empty dictionary to store financial data
    basis_data_all = {}

    # Fetch financial data for each symbol
    for symbol in tqdm(SYMBOLS, desc="Processing tickers"):

        # Create a yfinance Ticker object
        ticker = yf.Ticker(symbol)

        # Fetch financial data
        basis_data = fetch_all_basis_data(ticker=ticker)  # Fetch data once

        # Check if data was fetched successfully
        if basis_data is None:
            continue
        
        # Add the fetched data to the dictionary
        basis_data_all[symbol] = basis_data

    # Save data to file
    with open(os.path.join("downloads/basis_data_all.pkl"), "wb") as f:
        pickle.dump(obj=basis_data_all, file=f)

#%% Run the main function
if __name__ == "__main__":
    # Create downloads folder if it doesn't exist
    if not os.path.exists("downloads"):
        os.mkdir("downloads")

    main()

# %%
