from datetime import datetime, timedelta
import tzlocal

import formatter

class HttpStats:
    def __init__(self, time_window=0):
        self.log = []
        self.time_window = time_window

    def add(self, logline):
        self.log.append(logline)

    def top_pages(self, n, since):
        page_views = {}
        for logline in filter(lambda x: since is None or x.timestamp > since, self.log):
            section = logline.url
            if page_views.get(section) is not None:
                page_views[section] += 1
            else:
                page_views[section] = 1

        return sorted(page_views.items(), key=lambda x: -x[1])[:n]

    def total_pageviews(self, since):
        if since is not None:
            return len(list(filter(lambda x: x.timestamp > since, self.log)))
        else:
            return len(self.log)

    def num_unique_ips(self, since):
        return len(set([x.ip for x in filter(lambda x: since is None or x.timestamp > since, self.log)]))

    def __str__(self):
        since = None
        if self.time_window != 0:
            since = datetime.now(tzlocal.get_localzone()) - timedelta(0, self.time_window)
        out = ""
        if self.time_window == 0:
            out += "All time:\n"
        else:
            out += "Last {} seconds:\n".format(self.time_window)
        out += "---\n"
        out += "\n".join(["{}\t{}".format(views, page) for page, views in self.top_pages(10, since)])
        out += "\n---\n"
        out += "Page views: {}\n".format(self.total_pageviews(since))
        out += "Unique IPs: {}".format(self.num_unique_ips(since))
        return out
