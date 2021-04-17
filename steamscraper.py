# This script is for scraping the steam stats website
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
import os
from apscheduler.schedulers.background import BlockingScheduler

def steamscraper():
    # scrape the steam stats webpage
    URL = "https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics"
    steamstats = requests.get(URL)
    steamstats_soup = BeautifulSoup(steamstats.content, 'html.parser')
    gamesstats = steamstats_soup.find(id='detailStats')
    games = gamesstats.find_all('a', class_='gameLink')
    people = gamesstats.find_all('span', class_='currentServers')

    # create list of top 100 games

    game_list = list()
    for g in games:
        game_list.append(g.text)

    # zip people counts
    people_list = list()
    for p in people:
        people_list.append(int(int(p.text.replace(',', ''))))
    people_iter = iter(people_list)
    people_game_counts = [*zip(people_iter, people_iter)]
    people_game_counts = np.array(people_game_counts)

    # grab datetime
    time = datetime.now()

    game_database = pd.DataFrame(columns={'Date', 'Time', 'Game', 'CurrentPlayers', 'PeakPlayers'})
    game_database.Date = [time.strftime("%y/%m/%d")] * 100
    game_database.Time = [time.strftime("%H/%M/%S")] * 100
    game_database.Game = game_list
    game_database.CurrentPlayers = people_game_counts[:, 0]
    game_database.PeakPlayers = people_game_counts[:, 1]

    # create engine for pandas sql

    engine = create_engine(
        "mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="u$watchmenR15!", db="steamraces"))

    game_database.to_sql('counts', con=engine, if_exists="append")


# initalize scheduler
scheduler = BlockingScheduler()
scheduler.add_executor('processpool')
scheduler.add_job(steamscraper, 'interval', minutes=60)

steamscraper()