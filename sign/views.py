from django.contrib import admin
from django.shortcuts import render  # 这是默认的
from django.http import HttpResponse
"""
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("hello django")
"""
def index(request):
    return render(request, "index.html")
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username=='admin' and password=='admin123':
            return HttpResponse('login succse')
        else:
            return render(request,'index.html',{'error':'username or password error!'})
