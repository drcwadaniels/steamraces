# This script is for scraping the steam stats website
import requests
import pprint
from bs4 import BeautifulSoup
import numpy as np

#scrape the steam stats webpage
URL = "https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics"
steamstats = requests.get(URL)
steamstats_soup = BeautifulSoup(steamstats.content, 'html.parser')
gamesstats = steamstats_soup.find(id='detailStats')
games = gamesstats.find_all('a',class_='gameLink')
people = gamesstats.find_all('span', class_='currentServers')

#create list of top 100 games

game_list = list()
for g in games:
    game_list.append(g.text)

#zip people counts
people_list = list()
for p in people:
    people_list.append(p.text)
people_iter = iter(people_list)
people_game_counts = [*zip(int(people_iter), int(people_iter))]
print(people_game_counts)



