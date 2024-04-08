# %%

import pandas as pd

df_coins = pd.read_csv("../data/Coin_Raw/coin_Bitcoin.csv")
df_coins.head()
# %%
df_coins = df_coins.drop(['Symbol', 'SNo', 'Low', 'Open','Close', 'Name'], axis=1)
# %%
df_coins.head()

# %%

start_date = '2020-01-01'
end_date = '2020-12-31'

coins_filtered = df_coins[(df_coins['Date'] >= start_date) & (df_coins['Date'] <= end_date)]
# %%
df_coins = coins_filtered 

# %%
df_coins.reset_index(inplace=True, drop=True)
df_coins.head()
# %%
df_coins.to_csv('../data/Coin_Clean/coin_Bitcoin_clean.csv',index=False)