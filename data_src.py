
import pandas as pd
import numpy as np
import datetime as dt

# Replace the below file name for your layout if necessary
train_raw = pd.read_csv('data/train.csv')
train = train_raw # Todo:  Add split here

test_raw = pd.read_csv('data/test.csv')
test = test_raw

# date_time conversion
dates_dt = pd.to_datetime(train['date'])
dates_dt_min = dates_dt.min()
num_dates = (dates_dt.max() - dates_dt_min).days + 1
assert num_dates == 1688
raw_date_range = np.arange(num_dates)
date_range = pd.to_timedelta(raw_date_range, unit = 'days') + dates_dt_min
date_index = pd.DataFrame(data = raw_date_range, index = date_range)

families = train['family'].unique()
num_families = 33
assert families.shape == (num_families,)
fam_index = pd.DataFrame(data = np.arange(33), index = families)[0]

# Here's the conversion
train_txf = train.copy()
train_txf['date'] = pd.to_datetime(train['date'])
train_txf['day'] = (pd.to_datetime(train['date']) - dates_dt_min).dt.days
train_txf['store_nbr'] = train['store_nbr'] - 1
train_txf['family'] = train['family'].apply(fam_index.get)

num_stores = 54

# Allocate sales array
sales_shape = (1688, 54, 33)
sales = np.zeros(dtype = np.float64, shape = sales_shape)

# Fill in the sales array
for row in train_txf.itertuples():
    day = row.day
    store = row.store_nbr
    fam = row.family
    sales[day, store, fam] = row.sales

total_sales = sales.reshape(num_dates, num_stores * num_families)
total_sales_shape = total_sales.shape

# Oil Info

oil_df = pd.read_csv('data/oil.csv')
oil_txf = oil_df.copy()
oil_txf['date'] = pd.to_datetime(oil_df['date'])
oil_txf['day_num'] = (oil_txf['date'] - dates_dt_min).dt.days
oil_txf.set_index('day_num')

# def get_oil_price(date : dt.datetime):
#     # print(date)
#     # print(date.day_of_week)
#     tgt = date
#     if date.day_of_week == 5:
#         tgt = date - dt.timedelta(days = 1)
#     if date.day_of_week == 6:
#         tgt = date - dt.timedelta(days = 2)
#     # print(tgt)
#     price = oil_txf[oil_txf['date'] == tgt]['dcoilwtico'].iloc[0]
#     return price

# time_arange = np.arange(1688)
oil_filled = pd.DataFrame(index = raw_date_range, data = {
    'day_num' : raw_date_range,
    'day' : pd.to_timedelta(raw_date_range, unit = 'days')
})
oil_filled['date'] = oil_filled['day'] + dates_dt_min
oil_filled['price'] = oil_filled['day_num'].apply(oil_txf['dcoilwtico'].get).ffill()

oil_shape = (num_dates,)
oil = oil_filled['price'].values
assert oil.shape == oil_shape

# Holiday Info

# Not entered yet.
