import re
from datetime import datetime

from fast_strptime import fast_strptime

class HttpLog:
    log_re = re.compile(r"(\S+)\s(\S+)\s(\S+)\s\[([^\]]+)\]\s\"([A-Z]+)\s(\S+)\sHTTP\/(\d+\.\d+)\"\s(\d+)\s(\d+)")

    def __init__(self, ip, user_identifier, user_id, timestamp, method, url, http_version, status, size):
        self.ip = ip
        self.user_identifier = user_identifier
        self.user_id = user_id
        self.timestamp = timestamp
        self.method = method
        self.url = url
        self.http_version = http_version
        self.status = status
        self.size = size

    @classmethod
    def from_str(cls, log_line):
        match = cls.log_re.match(log_line)
        if match:
            try:
                timestamp = fast_strptime(match.group(4))
            except ValueError:
                return None
            if timestamp:
                return cls(
                        match.group(1),
                        match.group(2),
                        match.group(3),
                        timestamp,
                        match.group(5),
                        match.group(6),
                        match.group(7),
                        match.group(8),
                        int(match.group(9)))
        else:
            #TODO(Wesley) Log error
            return None

