#!/usr/bin/env python3

import sys
from datetime import datetime, timedelta

from httplog import HttpLog
from httpstats import HttpStats

def main():
    input_file = open(sys.argv[1], "r")
    stats = HttpStats()
    last_update = datetime(1,1,1) #TODO(Wesley) this is a hack
    up_to_date = False

    while True:
        line_str = input_file.readline()
        logline = HttpLog.from_str(line_str)
        if line_str:
            if logline:
                stats.add(logline)
            up_to_date = False
        else:
            up_to_date = True
        if up_to_date and datetime.now() - last_update > timedelta(0,1): #TODO(Wesley) allow configuring time
            stats.print_stats()
            last_update = datetime.now()

if __name__ == "__main__":
    main()
