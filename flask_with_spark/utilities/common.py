import time
import nltk
from datetime import datetime as dt


def utc_now_ts():
    d = dt.utcnow()
    epoch = dt(1970, 1, 1)
    t = (d - epoch).total_seconds()
    return int(t)


def calculate_distance(query, lst):
    return sorted(lst, key=lambda x: nltk.edit_distance(query, x))
