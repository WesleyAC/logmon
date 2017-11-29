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

## `alerts.py`

`alerts.py` provides a few classes - the main one is `AlertManager`, which triggers and keeps track of alerts. It expects the main loop to regularly call `update` with the number of hits that have occurred, keeping the alerting logic simple.

## `httpstats.py`

`httpstats.py` provides `HttpStats`, which keeps track of the line of the HTTP log, and can calculate statistics about them on-demand. I chose the model of keeping a simple list of events and calculating the stats later to simplify the process of adding more statistics - it could be more performant if bookkeeping was done on the stats when `HttpLog`s were added to the `HttpStats` object, but this would complicate the implementation more than it is worth.

## Improvements

`logmon` could be improved in a few ways:

* It's UI is somewhat lacking (a better way of viewing alerts would be good)
* It's not as performant as it could be - some ways to improve this are given in the `httpstats.py` section above and in [`docs/pref.md`](./perf.md)
* It's not as well-tested as it should be. Some end-to end tests would be good, particularly for the alerting and stats logic, and the W3C-formatted log parser could do with being tested on more inputs (this could be a good application of property-based testing).
