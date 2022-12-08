'''generate synthetic data from Heart Disease Cleavland dataset '''

import pandas as pd
import random

data = pd.read_csv('data_train.csv', header = 0, index_col = 0)
new_data = pd.DataFrame()
DATA_SIZE = 300

float_fields = ['oldpeak']
for field in data.columns.values:
    temp = []
    for i in range(DATA_SIZE):
        if field in float_fields:
            temp.append(random.uniform(data[field].min(), data[field].max()))
        else:
            temp.append(random.randint(data[field].min(), data[field].max()))
    new_data[field] = temp

new_data.to_csv('synthetic_data.csv')