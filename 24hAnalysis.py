import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from labellines import labelLine, labelLines
from sqlalchemy import create_engine
import sqlalchemy

# establish engine for pulling data
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="",
                                                                           db="steamraces"))

# pull data with pandas
tabbed_data = pd.read_sql("""SELECT * FROM steamraces.counts""", con=engine)

current_users_by_game = tabbed_data.groupby(['Game', 'Time']).sum() \
    .groupby(level=0).cumsum().reset_index()
min_current_users_by_game = current_users_by_game.groupby(['Game']).min().reset_index().sort_values(
    by=['CurrentPlayers'], ascending=False)
max_current_users_by_game = current_users_by_game.groupby(['Game']).max().reset_index().sort_values(
    by=['CurrentPlayers'], ascending=False)


i = 0
i2 = 1
label = []
plt1 = plt.figure(figsize=(22, 8))
for game in max_current_users_by_game.Game.unique():
    label.append(game)
    i += 1
    if i == 21:
        i = 1
        i2 += 1
    if i <= 10:
        m = "o"
    elif i >= 11:
        m = "*"
    plt.subplot(2, 4, i2)
    plt.plot(current_users_by_game.CurrentPlayers[current_users_by_game['Game'] == game].to_numpy()/
             min_current_users_by_game.CurrentPlayers[min_current_users_by_game['Game'] == game].to_numpy(),
             alpha=0.2, marker=m, label=game)
    if i2 == 1 or i2 == 5:
        plt.ylabel('Cumulative Sum of the Proportion of Players Above Hour 0')
    if i2 >= 5:
        plt.xlabel('Ordinal Hour: Hour 0 = First Appearance in Top 100')
    plt.legend(bbox_to_anchor=(1.7, 0.8, 0.3, 0.2), loc='upper right', prop={'size':7.5})
plt.subplots_adjust(wspace=1.15)
plt.tight_layout()
# get matplotlib baxkend so figures are saved max size
plt.savefig("RelativePlayers.png")



i = 0
i2 = 1
label = []
plt2 = plt.figure(figsize=(22, 8))
for game in max_current_users_by_game.Game.unique():
    label.append(game)
    i += 1
    if i == 21:
        i = 1
        i2 += 1
    if i <= 10:
        m = "o"
    elif i == 11:
        m = "*"
    plt.subplot(2, 4, i2)
    plt.plot(current_users_by_game.CurrentPlayers[current_users_by_game['Game'] == game].to_numpy(),
             alpha=0.2, marker=m, label=game)
    if i2 == 1 or i2 == 5:
        plt.ylabel('Cumulative Sum of Current Players')
    if i2 >= 5:
        plt.xlabel('Ordinal Hour: Hour 0 = First Appearance in Top 100')
    plt.legend(bbox_to_anchor=(1.7, 0.8, 0.3, 0.2), loc='upper right', prop={'size':7.5})
plt.subplots_adjust(wspace=1.15)
plt.tight_layout()
plt.savefig("AbsolutePlayers.png")
