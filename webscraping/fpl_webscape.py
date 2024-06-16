import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://www.livefpl.net/leagues/523899'
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
row_list = soup.find_all("tr")

team_list = []
manager_list = []
total_list = []
gw_net_list = []

game_week = None

for row in row_list:
    manager_name = row.find("p", class_="table-user-name")

    if manager_name:
        team_name = row.find("h3", class_="table-team-name")
        total = row.find("td", class_="table-total")
        gw_net = row.find("td", class_="table-gameweek")

        if not game_week:
            link = row.find("a")
            game_week = (str(link).split(' ')[1]).split('/event/')[1].replace('"', '')

        team_list.append(team_name.text)
        manager_list.append(manager_name.text)
        total_list.append(total.text)
        gw_net_list.append(gw_net.text)

entries = pd.DataFrame({'Team': team_list, 'Manager': manager_list, 'Total': total_list, 'GW Net': gw_net_list})

file = f'fpl_data_gw{game_week}.xlsx'
entries.to_excel(file, index=False)
