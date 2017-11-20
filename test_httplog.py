import pytest

from datetime import datetime, timezone, timedelta

from httplog import HttpLog

class TestHttpLog:
    def test_parse_fails(self):
        parse_failures = [
                "",
                '127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200', # missing field (size)
                '127.0.0.1 user-identifier frank [10-Oct-2000 13:55:36] "GET /apache_pb.gif HTTP/1.0" 200 1234', # Date format
                '127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] GET /apache_pb.gif HTTP/1.0 200 1234', # missing quotes
                '127.0.0.1 frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 1234', # missing user-id
        ]
        for line in parse_failures:
            print(line)
            assert HttpLog.from_str(line) is None

    def test_parses(self):
        # TODO(Wesley) Test more edge cases
        logline = HttpLog.from_str('127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326')
        assert logline.ip == "127.0.0.1"
        assert logline.user_identifier == "user-identifier"
        assert logline.user_id == "frank"
        assert logline.timestamp.timestamp() == datetime(2000, 10, 10, 13, 55, 36, tzinfo=timezone(timedelta(-1, 61200))).timestamp()
        assert logline.method == "GET"
        assert logline.url == "/apache_pb.gif"
        assert logline.status == "200"
        assert logline.size == 2326

