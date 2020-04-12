import requests
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + '/Data/'
if not(os.path.exists(data_path)):
    os.mkdir(data_path)
csv_file_path = dir_path + '/Data/COVID-19-DailyData.csv'


def is_older_than_today(filename):
    creationTime = os.path.getctime(filename)
    creationDate = datetime.date.fromtimestamp(creationTime)
    todaysDate = datetime.date.today()
    return creationDate < todaysDate


url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
if not(os.path.exists(csv_file_path)) or is_older_than_today(csv_file_path):
    r = requests.get(url, allow_redirects=True)
    with open(csv_file_path, 'wb') as csv:
        csv.write(r.content)


df = pd.read_csv(csv_file_path, engine='python')
sum_df = df.groupby(['countriesAndTerritories', 'popData2018'])[
    ['cases', 'deaths']].apply(sum)
# Removing these ones as they're not countries
sum_df = sum_df.drop(
    ['Cases_on_an_international_conveyance_Japan', 'San_Marino', 'Guernsey'], axis=0)
sum_df.reset_index(inplace=True)

sum_df['Cases%'] = (sum_df['cases'] / sum_df['popData2018']) * 100
sum_df['Deaths%'] = (sum_df['deaths'] / sum_df['popData2018']) * 100

top10_df = sum_df.nlargest(10, 'Deaths%')
plt.plot(top10_df['countriesAndTerritories'],
         top10_df['Deaths%'], marker='o', color='red')

for x, y in zip(top10_df['countriesAndTerritories'], top10_df['Deaths%']):
    plt.annotate(str(round(y, 4)) + "%", xy=(x, y))
plt.title("Countries with the Top 10 worst COVID-19 death rates")
plt.xlabel("Country")
plt.ylabel("Percentage of Population")
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.grid()
plt.show()
