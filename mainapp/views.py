import datetime
import threading

from django.shortcuts import render, redirect
from twisted.internet.threads import deferToThread

from mainapp import models
from mainapp.utils import md5_util

from mainapp.utils.all_map import AllMap

all_map = AllMap()
data = {}
index_h = "278px"
index_w = "434px"
data["spider_time"] = all_map.spider_time
data["p1"] = all_map.get_p1("610px", "900px")
data["p2"] = all_map.get_p2()
data["p3"] = all_map.get_p3()
data["p4"] = all_map.get_p4(index_h, index_w)
data["p5"] = all_map.get_p5(index_h, index_w)
data["p6"] = all_map.get_p6(index_h, index_w)
data["p7"] = all_map.get_p7(index_h, "898px")
data["p8"] = all_map.get_p8(index_h, index_w)

page_h = "753px"
page_w = "1328px"
is_show = True
p1 = all_map.get_p1(page_h, page_w, is_show)
p4 = all_map.get_p4(page_h, page_w, is_show)
p5 = all_map.get_p5(page_h, page_w, is_show)
p6 = all_map.get_p6(page_h, page_w, is_show)
p7 = all_map.get_p7(page_h, page_w, is_show)
p8 = all_map.get_p8(page_h, page_w, is_show)

map_list = {"长沙景点分布":p1, "景点评分数据": data["p2"], "景点浏览人数": data["p3"], "景点人数分布": p4, "景点评论词云": p5, "景点浏览时间": p6, "景点数量": p7, "景点评分": p8}

def index(request):
    return render(request, "index.html", data)


def page(request):
    result = {
        "is_chart": True,
        "spider_time": all_map.spider_time
    }
    page = request.GET.get("p")
    if not page:
        page = 0
    else:
        page = int(page) - 1
    result["title"] = list(map_list.keys())[page]
    result['data'] = map_list.get(result["title"])
    result['page_data'] = map_list
    if page in [1,2]:
        result["is_chart"] = False
    return render(request, 'page/index.html', result)


"""
登陆
"""
def login(request):
    temp_txt = {
        "tip": "请登录",
        "username": "用户名",
        "password": "密码",
        "remember": "记住密码",
        "login": "登陆",
        "go": "去注册",
        "year": datetime.datetime.now().year,
        "next_year": int(datetime.datetime.now().year) + 1,
        "error": ''
    }
    if request.method == 'GET':
        return render(request, "login.html", temp_txt)
    if request.method == 'POST':
        #请求登陆
        concat = request.POST
        username = concat["username"]
        password = md5_util.md5(concat["password"])
        user = models.Userinfo.objects.filter(username=username, password=password).first()
        if user:
            request.session.setdefault("user_info", username)
            return redirect("/index")
        else:
            request.method = "GET"
            temp_txt['error'] = "用户名或密码错误"
            return render(request, "login.html", temp_txt)

"""
注册
"""
def register(request):
    temp_txt = {
        "tip": "注册用户",
        "username": "用户名",
        "password": "密码",
        "login": "注册",
        "go": "去登陆",
        "year": datetime.datetime.now().year,
        "next_year": int(datetime.datetime.now().year) + 1,
        'error':''
    }
    if request.method == 'GET':
        return render(request, "register.html", temp_txt)


    elif request.method == 'POST':
        # 注册请求接口
        # 获取用户名和密码
        concat = request.POST
        username = concat["username"]
        password = concat["password"]
        repassword = concat["repassword"]
        if 3 > len(username) > 16:
            temp_txt["error"] = "用户名过长或过短！"
        elif repassword != password:
            temp_txt['error'] = "密码不一致！"
        elif models.Userinfo.objects.filter(username=username).first():
            temp_txt['error'] = "用户名已存在！"
        elif 16 < len(password) or len(password) < 6:
            temp_txt["error"] = "密码长度小于6或大于16"
        if temp_txt['error']:
            request.method = "GET"
            return render(request, 'register.html', temp_txt)

        # 加密
        password = md5_util.md5(password)

        result = models.Userinfo.objects.create(username=username, password=password)
        print(f"result:{result}")
        return redirect("/login")

