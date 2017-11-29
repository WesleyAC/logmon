# `logmon`

![screenshot](./docs/screenshot.png)

`logmon` is a program to ingest a W3C-formatted HTTP access log and display stats about it.

# Usage

`./main.py /path/to/access.log`

Optional arguments:

| Argument          | Description |
| ----------------- | --- |
| -h, --help        | show the help message and exit |
| --time-window     | what time window to view stats over (seconds, default=∞) |
| --update-interval | how often to update the screen (seconds, default=10) |
| --alert-window    | what time window to use for high traffic alerts (seconds, default=120) |
| --alert-threshold | how many pageviews need to occur in the alert_window to trigger an alert (default=500) |

# Features

* Displays top pages
* Alerts when total traffic goes over a certain value
* Shows total number of pageviews
* Shows the number of unique IP addresses in the log
