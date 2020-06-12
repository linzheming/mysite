from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.
from django.template import loader

from .models import Cookies

from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cookies.serializers import CookiesSerializer

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)  # <-- And here
    def get_ip_ua(self, request, obj):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')

        obj.ua = user_agent
        obj.ip  = ipaddress
        obj.save()

    def get(self, request):
        cookies = Cookies.objects.all()
        serializer = CookiesSerializer(cookies, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("-------- post ---------")
        print(request.data)
        serializer = CookiesSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            # get ip
            self.get_ip_ua(request, obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)