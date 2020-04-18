import numpy as np
import matplotlib.pyplot as plt
import requests
import os
import datetime
import pandas as pd
pd.set_option('display.max_columns', None)


dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + '/Data/'
if not(os.path.exists(data_path)):
    os.mkdir(data_path)
csv_file_path = dir_path + '/Data/Ontario-COVID-19-Data.csv'


def is_older_than_today(filename):
    modifiedTime = os.path.getmtime(filename)
    modifiedDate = datetime.date.fromtimestamp(modifiedTime)
    todaysDate = datetime.date.today()
    return modifiedDate < todaysDate


# Scraping the website for data if need be
url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'
if not(os.path.exists(csv_file_path)) or is_older_than_today(csv_file_path):
    r = requests.get(url, allow_redirects=True)
    with open(csv_file_path, 'wb') as csv:
        csv.write(r.content)

# Dataframe manipulation
df = pd.read_csv(csv_file_path, engine='python')
df = df.iloc[:, 1:5]
df['Count'] = 1
sum_df = df.groupby('ACCURATE_EPISODE_DATE').sum()
sum_df.reset_index(inplace=True)
sum_df['Days'] = (pd.to_datetime(
    sum_df['ACCURATE_EPISODE_DATE']) - pd.to_datetime('2020-01-21')).dt.days

# Plotting
plt.figure(figsize=(10, 6))
ax = plt.axes()
ax.set_facecolor("grey")
plt.title("Ontario COVID-19 Cases Per Day")
plt.xlabel("Days since first ontario case (2020-01-21)")
plt.ylabel("Number of Cases")
plt.grid(zorder=0)
plt.plot(sum_df['Days'], sum_df['Count'], marker='o', color='red')
plt.rc('axes', axisbelow=True)
plt.xticks(np.arange(min(sum_df['Days']), max(sum_df['Days'])+1, 5))
savefigname = dir_path + "\\" + str(datetime.date.today()) + ".png"
plt.savefig(savefigname)
plt.show()
