#!/usr/bin/env python3

import random
import time
from datetime import datetime

import tzlocal

def main():
    ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4']
    urls = ["/url_a", "/url_b", "/url_c", "/url_d"]
    statuses = [200,]
    sizes = [1337,]
    while True:
        logline = '{ip} - - [{timestamp}] "GET {url} HTTP/1.0" {status} {size}'.format(ip=random.choice(ips), timestamp=tzlocal.get_localzone().localize(datetime.now()).strftime("%d/%b/%Y:%H:%M:%S %z"), url=random.choice(urls), status=random.choice(statuses), size=random.choice(sizes))
        print(logline)

if __name__ == "__main__":
    main()
