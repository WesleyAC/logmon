# `logmon` architecture overview

`logmon` is split up into a few files:

| File               | Description |
| ------------------ | ----------- |
| `main.py`          | Parses command line args, runs the main loop - ingesting lines from the file, adding them to the `HttpStats` object, and printing the stats |
| `httplog.py`       | Contains the `HttpLog` class, which represents a line in a HTTP access log |
| `httpstats.py`     | Keeps track of statistics about a HTTP log |
| `alerts.py`        | Generates and keeps track of alerts. |
| `formatter.py`     | Simple convenience functions for dealing with sending ANSI escape codes |
| `fast_strptime.py` | A version of strptime that only parses the default W3C HTTP access log format, but does so much faster than the builtin `strptime`. See [`docs/pref.md`](./perf.md) for more info. |
