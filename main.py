#!/usr/bin/env python3

import sys
import argparse
from datetime import datetime, timedelta
import shutil
import tzlocal

from httplog import HttpLog
from httpstats import HttpStats
from alerts import AlertManager
import formatter

def main(filename, time_window, update_interval, alert_window, alert_threshold):
    if filename != "-":
        input_file = open(filename, "r")
    else:
        input_file = sys.stdin
    stats = HttpStats(time_window)
    alert_manager = AlertManager(alert_threshold)
    last_update = datetime(1,1,1) #TODO(Wesley) this is a hack
    #TODO(Wesley) Should handle SIGWINCH and reset this value.
    # Another option would be to get this value in the main loop.
    term_height = shutil.get_terminal_size((80, 20))[1]

    while True:
        line_str = input_file.readline()
        if line_str:
            logline = HttpLog.from_str(line_str)
            if logline:
                stats.add(logline)
        elif datetime.now() - last_update > timedelta(0,update_interval):
            alert_manager.update(stats.total_pageviews(datetime.now(tzlocal.get_localzone()) - timedelta(0, alert_window)), datetime.now())
            formatter.clear_screen()
            stats_str = str(str(stats))
            print("")
            print(stats_str)
            lines_left = term_height - stats_str.count("\n") - 1
            print(alert_manager.to_str(lines_left), end="")
            sys.stdout.flush()
            last_update = datetime.now()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Show statistics about HTTP logs.')
    parser.add_argument('file', type=str, help='what file to read from')
    parser.add_argument('--time-window', type=int, default=0, help='what time window to view stats over (seconds, default=∞)')
    parser.add_argument('--update-interval', type=int, default=10, help='how often to update the screen (seconds, default=10)')
    parser.add_argument('--alert-window', type=int, default=120, help='what time window to use for high traffic alerts (seconds, default=120)')
    parser.add_argument('--alert-threshold', type=int, default=500, help='how many pageviews need to occur in the alert_window to trigger an alert (default=500)')

    args = parser.parse_args()
    main(args.file, args.time_window, args.update_interval, args.alert_window, args.alert_threshold)
