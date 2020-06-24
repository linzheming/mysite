#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'James'
from rest_framework import serializers
from .models import Cookies

# from .http_util import run_notify_in_thread

class CookiesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    c_user = serializers.CharField(max_length=30)
    text = serializers.CharField(max_length=3000)

    def create(self, validated_data):
        """
        Create and return a new `cookie` instance, given the validated data.
        """
        cookie, created = Cookies.objects.update_or_create(
            c_user=validated_data.get('c_user', None),
            defaults={'text': validated_data.get('text', None)})
        print("created "+ str(created))

        return cookie
        # return Cookies.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.c_user = validated_data.get('c_user', instance.code)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance