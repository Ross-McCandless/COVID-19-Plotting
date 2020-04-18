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


# scrapes the website if need be
url = 'https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv'
if not(os.path.exists(csv_file_path)) or is_older_than_today(csv_file_path):
    r = requests.get(url, allow_redirects=True)
    with open(csv_file_path, 'wb') as csv:
        csv.write(r.content)

# Dataframe manipulation
df = pd.read_csv(csv_file_path, engine='python')
df = df.iloc[:,  1:5]
df['Count'] = 1
sum_df = df.groupby(['Age_Group', 'CLIENT_GENDER']).sum()
sum_df.reset_index(inplace=True)
female_df = sum_df[sum_df.CLIENT_GENDER.isin(
    ['FEMALE']) & ~sum_df.Age_Group.isin(['Unknown'])]
female_df = pd.DataFrame(np.roll(female_df.values, 1, axis=0),
                         index=np.roll(female_df.index, 1), columns=female_df.columns)
female_df.reset_index(inplace=True)
male_df = sum_df[sum_df.CLIENT_GENDER.isin(
    ['MALE']) & ~sum_df.Age_Group.isin(['Unknown'])]
male_df = pd.DataFrame(np.roll(male_df.values, 1, axis=0),
                       index=np.roll(male_df.index, 1), columns=male_df.columns)
male_df.reset_index(inplace=True)


# Plotting
plt.figure(figsize=(10, 6))
ax = plt.axes()
ax.set_facecolor("grey")
plt.title("Ontario COVID-19 Cases by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Cases")
plt.grid(zorder=0)
p1 = plt.bar(male_df.index, male_df['Count'], zorder=3, color='skyblue')
p2 = plt.bar(female_df.index,
             female_df['Count'], bottom=male_df['Count'], zorder=3, color='pink')
plt.rc('axes', axisbelow=True)
plt.xticks(male_df.index, male_df['Age_Group'])
plt.legend((p1[0], p2[0]), ('Men', 'Women'))
savefigname = dir_path + "\\" + str(datetime.date.today()) + ".png"
plt.savefig(savefigname)
plt.show()
