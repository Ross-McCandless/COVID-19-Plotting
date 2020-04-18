import matplotlib.pyplot as plt
import datetime
import os
import requests
import pandas as pd
pd.set_option('display.max_columns', None)

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + '/Data/'
if not(os.path.exists(data_path)):
    os.mkdir(data_path)
csv_file_path = dir_path + '/Data/COVID-19-DailyData.csv'


def is_older_than_today(filename):
    modifiedTime = os.path.getmtime(filename)
    modifiedDate = datetime.date.fromtimestamp(modifiedTime)
    todaysDate = datetime.date.today()
    return modifiedDate < todaysDate


# scrapes the website if need be
url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
if not(os.path.exists(csv_file_path)) or is_older_than_today(csv_file_path):
    r = requests.get(url, allow_redirects=True)
    with open(csv_file_path, 'wb') as csv:
        csv.write(r.content)

# Dataframe manipulation
df = pd.read_csv(csv_file_path, engine='python')
sum_df = df.groupby(['countriesAndTerritories', 'popData2018', 'dateRep'])[
    ['cases', 'deaths']].apply(sum)
sum_df.reset_index(inplace=True)
sum_df['dateRep'] = pd.to_datetime(sum_df['dateRep'], format="%d/%m/%Y")
sum_df = sum_df.sort_values(by=['dateRep'])
dateCutOff = sum_df['dateRep'] > '2020-02-15'
sum_df = sum_df.loc[dateCutOff]
sum_df['cumcases'] = sum_df.groupby('countriesAndTerritories')[
    'cases'].transform(pd.Series.cumsum)
sum_df['PercentInfected'] = sum_df['cumcases'] / sum_df['popData2018'] * 100

canada_df = sum_df.loc[sum_df['countriesAndTerritories'].isin(['Canada'])]
us_df = sum_df.loc[sum_df['countriesAndTerritories'].isin(
    ['United_States_of_America'])]
germany_df = sum_df.loc[sum_df['countriesAndTerritories'].isin(['Germany'])]
italy_df = sum_df.loc[sum_df['countriesAndTerritories'].isin(['Italy'])]
japan_df = sum_df.loc[sum_df['countriesAndTerritories'].isin(['Japan'])]
united_kingdom_df = sum_df.loc[sum_df['countriesAndTerritories'].isin([
                                                                      'United_Kingdom'])]
france_df = sum_df.loc[sum_df['countriesAndTerritories'].isin(['France'])]


# plotting
plt.figure(figsize=(10, 5))
plt.figtext(0.01, 0.03, 'Source: www.ecdc.europa.eu',
            ha='left')
plt.plot(canada_df['dateRep'],
         canada_df['PercentInfected'], marker='o', color='red', label='Canada ({})'.format(canada_df['cumcases'].max()))
plt.plot(us_df['dateRep'],
         us_df['PercentInfected'], marker='o', color='blue', label='USA ({})'.format(us_df['cumcases'].max()))
plt.plot(germany_df['dateRep'],
         germany_df['PercentInfected'], marker='o', color='gold', label='Germany ({})'.format(germany_df['cumcases'].max()))
plt.plot(italy_df['dateRep'],
         italy_df['PercentInfected'], marker='o', color='green', label='Italy ({})'.format(italy_df['cumcases'].max()))
plt.plot(japan_df['dateRep'],
         japan_df['PercentInfected'], marker='o', color='darkorange', label='Japan ({})'.format(japan_df['cumcases'].max()))
plt.plot(united_kingdom_df['dateRep'],
         united_kingdom_df['PercentInfected'], marker='o', color='black', label='UK ({})'.format(united_kingdom_df['cumcases'].max()))
plt.plot(france_df['dateRep'],
         france_df['PercentInfected'], marker='o', color='pink', label='France ({})'.format(france_df['cumcases'].max()))
plt.legend(loc='upper center', title='Country (# of cases)')
plt.title("G7 Countries COVID-19 Infected Population (%) over time")
plt.xlabel("Date (from: 2020-02-15 to: {})".format(datetime.date.today()))
plt.ylabel("Infected Population (%)")
plt.xticks(rotation=20)
plt.grid()
plt.tight_layout()
savefigname = dir_path + "\\" + str(datetime.date.today()) + ".png"
plt.savefig(savefigname)
plt.show()
