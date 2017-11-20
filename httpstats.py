import formatter

class HttpStats:
    def __init__(self):
        self.log = []
        self.page_views = {}
        self.total_views = 0
        self.ips = set()
        self.unique_ips = 0

    def add(self, logline):
        self.log.append(logline)

        section = logline.url
        if self.page_views.get(section) is not None:
            self.page_views[section] += 1
        else:
            self.page_views[section] = 1

        self.total_views += 1

        if logline.ip not in self.ips:
            self.ips.add(logline.ip)
            self.unique_ips += 1

    def top_pages(self, n):
        return sorted(self.page_views.items(), key=lambda x: -x[1])[:n]

    def print_stats(self):
        formatter.clear_screen()
        print('\n'.join(["{}\t{}".format(views, page) for page, views in self.top_pages(10)]))
