#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'James'

import requests

#通知该ip已经转换
# http://fuckbook.network/t/pixelbyip.php?ip=yourip&payout=0.5
def notify_ok_http_get(ip):
    url = "http://fuckbook.network/t/pixelbyip.php"
    data = {
        'ip': ip,
        'payout': 0.5
    }

    try:
        r = requests.get(url, params=data, timeout=0.5)
    except requests.RequestException as e:
        print("notify_ok_http_get OOps: ", e)
        return
    print("notify_ok ok")
