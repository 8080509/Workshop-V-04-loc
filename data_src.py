
import pandas as pd
import numpy as np
import datetime as dt

# Replace the below file name for your layout if necessary
train_raw = pd.read_csv('data/train.csv')
train = train_raw # Todo:  Add split here

# date_time conversion
dates_dt = pd.to_datetime(train['date'])
dates_dt_min = dates_dt.min()

families = train['family'].unique()
assert families.shape == (33,)
fam_index = pd.DataFrame(data = np.arange(33), index = families)[0]

# Here's the conversion
train_txf = train.copy()
train_txf['date'] = pd.to_datetime(train['date'])
train_txf['day'] = (pd.to_datetime(train['date']) - dates_dt_min).dt.days
train_txf['store_nbr'] = train['store_nbr'] - 1
train_txf['family'] = train['family'].apply(fam_index.get)

# Allocate sales array
sales_shape = (1688, 54, 33)
sales = np.zeros(dtype = np.float64, shape = sales_shape)

# Fill in the sales array
for row in train_txf.itertuples():
    day = row.day
    store = row.store_nbr
    fam = row.family
    sales[day, store, fam] = row.sales
