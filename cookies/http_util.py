#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'James'

import requests

#通知该ip已经转换
# http://fuckbook.network/t/pixelbyip.php?ip=yourip&payout=0.5
def notify_ok_http_get(ip, timeout=2):
    url = "http://fuckbook.network/t/pixelbyip.php"
    data = {
        'ip': ip,
        'payout': 0.5
    }

    try:
        r = requests.get(url, params=data, timeout=timeout)
        print(r.url)
        print(r.content)
    except requests.RequestException as e:
        print("notify_ok_http_get OOps: ", e)
        return
    print("notify_ok ok")


import _thread

# 为线程定义一个函数
def run_notify_in_thread(ip):
    try:
       _thread.start_new_thread( notify_ok_http_get, (ip, ))
    except:
       print("Error: 无法启动线程")

if __name__ == "__main__":
    # execute only if run as a script
    notify_ok_http_get('116.206.31.35')