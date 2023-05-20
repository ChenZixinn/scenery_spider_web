from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class UserAuth(MiddlewareMixin):
    def process_request(self, request):
        # print(request.path_info)
        if request.path_info in ["/login/", "/register/", "/login.html", "/", '/img/code/', '/index/login.html']:
            return
        user_info = request.session.get("user_info")
        if user_info:
            return

        return redirect("/login")
