#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'James'
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

from . import views

urlpatterns = [
    # python manage.py drf_create_token vitor  发现token每次都一样
    # http http://127.0.0.1:8000/cookies/hello/ 'Authorization: Token 379a9d99cc181dcbbceb602b238a6838e4bc1b59'
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('geturls/', views.GetUrlsView.as_view(), name='geturls'),
    path('', views.index, name='index'),
    # http post http://127.0.0.1:8000/cookies/api-token-auth/ username=vitor password=Qwer1234
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
]