#!/usr/bin/env python3

import sys
import argparse
from datetime import datetime, timedelta

from httplog import HttpLog
from httpstats import HttpStats

def main(filename, time_window, update_interval):
    input_file = open(filename, "r")
    stats = HttpStats(time_window)
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
        if up_to_date and datetime.now() - last_update > timedelta(0,update_interval):
            stats.print_stats()
            last_update = datetime.now()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Show statistics about HTTP logs.')
    parser.add_argument('file', type=str, help='what file to read from')
    parser.add_argument('--time-window', type=int, default=0, help='what time window to view stats over (seconds, default=∞)')
    parser.add_argument('--update-interval', type=int, default=10, help='how often to update the screen (seconds, default=10)')

    args = parser.parse_args()
    main(args.file, args.time_window, args.update_interval)
