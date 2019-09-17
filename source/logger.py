"""
Logging functions
"""
import datetime
logfile = 'log.txt'


def tee(*items):
    """
    Log item to console and to file
    :param item: String to log
    :return: None
    """
    fin = ""
    for item in items:
        fin = fin + str(item)
    with open(logfile, "a") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S: ") + fin + "\n")
    print(fin)
