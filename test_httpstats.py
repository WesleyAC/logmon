import pytest

from datetime import datetime, timezone, timedelta

from httpstats import HttpStats
from httplog import HttpLog

def gen_log_for_page(page, ip="127.0.0.1"):
    return HttpLog.from_str('{} user-identifier userid [10/Oct/2000:13:55:36 -0700] "GET {} HTTP/1.0" 200 1234'.format(ip, page))

class TestHttpLog:
    def test_all_time_top_pages(self):
        stats = HttpStats()
        for i in range(100):
            stats.add(gen_log_for_page("/page_a"))
        for i in range(200):
            stats.add(gen_log_for_page("/page_b"))
        for i in range(300):
            stats.add(gen_log_for_page("/page_c"))
        top2 = stats.top_pages(2, None)
        assert len(top2) == 2
        assert top2[0] == ("/page_c", 300)
        assert top2[1] == ("/page_b", 200)

    def test_all_time_pageviews(self):
        stats = HttpStats()
        for _ in range(100):
            stats.add(gen_log_for_page("/foobar"))
        assert stats.total_pageviews(None) == 100
        for _ in range(100):
            stats.add(gen_log_for_page("/foobar"))
        assert stats.total_pageviews(None) == 200

    def test_all_time_unique_ips(self):
        stats = HttpStats()
        for i in range(100):
            stats.add(gen_log_for_page("/foobar", ip="10.0.0.{}".format(i)))
            stats.add(gen_log_for_page("/foobar", ip="10.0.0.{}".format(i)))
        assert stats.num_unique_ips(None) == 100
        for i in range(100):
            stats.add(gen_log_for_page("/foobar", ip="10.0.0.{}".format(i)))
        assert stats.num_unique_ips(None) == 100
        for i in range(100):
            stats.add(gen_log_for_page("/foobar", ip="10.1.0.{}".format(i)))
        assert stats.num_unique_ips(None) == 200
