#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install requests pandas')


# In[2]:


import requests
import pandas as pd
from datetime import datetime, timedelta

# Define the base URL and parameters
base_url = 'https://api.coingecko.com/api/v3/coins/{id}/market_chart'
params = {
    'vs_currency': 'usd',
    'days': 7  # last 7 days
}

# List of cryptocurrency IDs to fetch data for (top 10 by market cap)
crypto_ids = ['bitcoin', 'ethereum', 'tether', 'binancecoin', 'cardano', 
              'ripple', 'dogecoin', 'usd-coin', 'polkadot', 'uniswap']

# Function to fetch and process data for each cryptocurrency
def fetch_data(crypto_id):
    url = base_url.format(id=crypto_id)
    response = requests.get(url, params=params)
    data = response.json()
    
    # Check if 'prices', 'market_caps', and 'total_volumes' exist
    if 'prices' in data and 'market_caps' in data and 'total_volumes' in data:
        prices = data['prices']
        market_caps = data['market_caps']
        total_volumes = data['total_volumes']
    
        # Convert to DataFrame
        df_prices = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df_market_caps = pd.DataFrame(market_caps, columns=['timestamp', 'market_cap'])
        df_volumes = pd.DataFrame(total_volumes, columns=['timestamp', 'volume'])
    
        # Merge DataFrames on timestamp
        df = df_prices.merge(df_market_caps, on='timestamp').merge(df_volumes, on='timestamp')
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['crypto'] = crypto_id
        return df
    else:
        print(f"Error fetching data for {crypto_id}: {data}")
        return pd.DataFrame()

# Fetch data for all cryptocurrencies and combine into a single DataFrame
all_data = pd.concat([fetch_data(crypto_id) for crypto_id in crypto_ids])

# Save to CSV
all_data.to_csv('crypto_data_extended.csv', index=False)

print("Data has been saved to crypto_data_extended.csv")


# In[ ]:




