from admin_numeric_filter.admin import RangeNumericFilter, NumericFilterModelAdmin
from django.contrib import admin


# 增加一个导出 model 为 csv 的 action
import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many \
              and not field.one_to_many]
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


export_to_csv.short_description = 'Export to CSV'

# Register your models here.

from .models import Cookies

@admin.register(Cookies)
class CookiesAdmin(NumericFilterModelAdmin):
    list_display = ('id', 'c_user', 'json_format', 'ip', 'ua', 'created', 'updated',)
    list_filter = ('created',('id', RangeNumericFilter), )
    # list_filter = ('created',('id', RangeNumericFilter), 'country')
    search_fields = ('c_user',)
    ordering = ('created',)
    actions = [export_to_csv]

    #  in the forms on the “add” and “change” pages
    fields = ('c_user', 'text')

    # list_per_page = 50

