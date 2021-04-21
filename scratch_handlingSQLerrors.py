# keeping this for later as it was decent way to handle errors one receives when there is yet an SQL dB

def get_entries():  # function for getting initial value of those global vars
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",
                                                                               pw="u$watchmenR15!", db="steamraces"))
    try:
        entries = pd.read_sql('SELECT DISTINCT(Day) FROM steamraces.counts', con=engine)
        dnum = entries.iloc[-1].to_numpy()
    except sqlalchemy.exc.ProgrammingError as e:
        print("No days")
        dnum = 0

    try:
        entries = pd.read_sql('SELECT DISTINCT(Hour) FROM steamraces.counts', con=engine)
        hnum = entries.iloc[-1].to_numpy()
    except sqlalchemy.exc.ProgrammingError as e:
        print("No hours")
        hnum = -1
    return dnum, hnum


# get entries for indexing
day, hour = get_entries()
print("starting at day:", day, "and hour:", hour+1)
