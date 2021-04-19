# This script is for scraping the steam stats website
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import sqlalchemy
from apscheduler.schedulers.background import BlockingScheduler
import logging


def steamscraper(d, h):
    h = h + 1  # increment hour

    if h == 25:  # catch if in the next day (24 hour epoc)
        h = 1
        d = d + 1

    # scrape the steam stats webpage
    print("Steam scraper for entry:", d, h)
    url = "https://store.steampowered.com/stats/Steam-Game-and-Player-Statistics"
    steamstats = requests.get(url)
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

    game_database = pd.DataFrame(columns={'Day', 'Hour', 'Date', 'Time', 'Game', 'CurrentPlayers', 'PeakPlayers'})
    game_database.Day = np.repeat(d, 100)
    game_database.Hour = np.repeat(h, 100)
    game_database.Date = [time.strftime("%y/%m/%d")] * 100
    game_database.Time = [time.strftime("%H/%M/%S")] * 100
    game_database.Game = game_list
    game_database.CurrentPlayers = people_game_counts[:, 0]
    game_database.PeakPlayers = people_game_counts[:, 1]

    # create engine for pandas sql

    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="",
                                                                               db="steamraces"))

    game_database.to_sql('counts', con=engine, if_exists="append")
    print("Steam scraper finished for entry:", d, h)


# index entries to sql server
def get_entries():
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",
                                                                               pw="",db="steamraces"))
    try:
        entries = pd.read_sql('SELECT DISTINCT(Day) FROM steamraces.counts', con=engine)
        d = entries.iloc[-1].to_numpy()
    except sqlalchemy.exc.ProgrammingError as e:
        print("No days")
        d = 0

    try:
        entries = pd.read_sql('SELECT DISTINCT(Hour) FROM steamraces.counts', con=engine)
        h = entries.iloc[-1].to_numpy()
    except sqlalchemy.exc.ProgrammingError as e:
        print("No hours")
        h = 0
    return d, h


# get entries for indexing
d, h = get_entries()


# scheduler
if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = BlockingScheduler()
    scheduler.add_job(lambda: steamscraper(d, h), 'interval', minutes=60, replace_existing=True)
    if d == 0 and h == 0:
        steamscraper(d, h)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # keeping things alive, as we know it; and I feel fine!
        while True:
            time.sleep(58)
    except (KeyboardInterrupt, SystemExit):
        # kill this program
        scheduler.shutdown()
