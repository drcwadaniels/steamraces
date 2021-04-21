import numpy as np
import pandas as pd
import matplotlib as plt
from sqlalchemy import create_engine
import pymysql
import os
from apscheduler.schedulers.background import BlockingScheduler
import logging
from datetime import datetime


# establish engine for pulling data
# engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="u$watchmenR15!", db="steamraces"))

# calculate range of data
yesterday = datetime.now() - datetime.timedelta(days=1)

print(yesterday)
