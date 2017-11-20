import pytest

from datetime import datetime, timezone, timedelta

from httpstats import HttpStats
from httplog import HttpLog

def gen_log_for_page(page):
    return HttpLog.from_str('127.0.0.1 user-identifier userid [10/Oct/2000:13:55:36 -0700] "GET {} HTTP/1.0" 200 1234'.format(page))

class TestHttpLog:
    def test_top_pages(self):
        stats = HttpStats()
        for i in range(100):
            stats.add(gen_log_for_page("/page_a"))
        for i in range(200):
            stats.add(gen_log_for_page("/page_b"))
        for i in range(300):
            stats.add(gen_log_for_page("/page_c"))
        top2 = stats.top_pages(2)
        assert len(top2) == 2
        assert top2[0] == ("/page_c", 300)
        assert top2[1] == ("/page_b", 200)
