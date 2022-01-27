import datetime


def get_min_timestamp():
    return (datetime.datetime.now() - datetime.timedelta(minutes=15)).timestamp()
