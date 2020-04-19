import requests
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

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
sum_df = df.groupby(['countriesAndTerritories', 'popData2018'])[
    ['cases', 'deaths']].apply(sum)
sum_df.reset_index(inplace=True)
G7Countries = ['Canada', 'United_States_of_America',
               'France', 'Italy', 'Japan', 'United_Kingdom', 'Germany']
sum_df = sum_df.loc[sum_df['countriesAndTerritories'].isin(G7Countries)]
sum_df['DeathRate'] = (sum_df['deaths'] / sum_df['cases']) * 100
G7Countries_df = sum_df.nlargest(7, 'DeathRate')
print(G7Countries_df)


# plotting
plt.plot(G7Countries_df['countriesAndTerritories'],
         G7Countries_df['DeathRate'], marker='o', color='red')
for x, y in zip(G7Countries_df['countriesAndTerritories'], G7Countries_df['DeathRate']):
    plt.annotate(str(round(y, 2)) + "%", xy=(x, y))
plt.title("G7 Countries COVID-19 death rates")
plt.xlabel("Country")
plt.ylabel("Death Rate (%)")
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.xticks(rotation=30)
plt.grid()
plt.tight_layout()
savefigname = dir_path + "\\" + str(datetime.date.today()) + ".png"
plt.savefig(savefigname)
plt.show()
