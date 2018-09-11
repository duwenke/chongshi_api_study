from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
"""
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("hello django")
"""
def index(request):
    return render(request, "index.html")
# def login_action(request):
#     if request.method == 'POST':
#         username = request.POST.get('username','')
#         password = request.POST.get('password','')
#         if username=='admin' and password=='admin123':
#             return HttpResponse('login succse')
#         else:
#             return render(request,'index.html',{'error':'username or password error!'})
''''
# 引入新类HttpResponseRedirect，可以对路径进行重定向，将登录成功请求指向event_manage
# 也就是：http://127.0.0.1:8000/event_manage/
#登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username=='admin' and password=='admin123':
            return HttpResponseRedirect('/event_manage/')
        else:
            return render(request,'index.html',{'error':'username or password error!'})
#发布会管理
def event_manage(request):
    return render(request,'event_manage.html')

'''

'''
#cookied的使用
#登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username=='admin' and password=='admin123':
            response=HttpResponseRedirect('/event_manage/')
            response.set_cookie('user',username,3600) # 浏览器添加cookie
            return response
            # set_cookie参数说明：1、user表示写入浏览器的cookie名
            #                    2、username是用户在登录页输入的用户名
            #                    3、3600是设置cookie在浏览器中的保持时间，默认为秒

        else:
            return render(request,'index.html',{'error':'username or password error!'})
#发布会管理
def event_manage(request):
    username=request.COOKIES.get('user', '') # 读取浏览器cookie
    return render(request,'event_manage.html',{'user':username})
'''
'''
# session的使用
#登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if username=='admin' and password=='admin123':
            response=HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user',username,3600) # 浏览器添加cookie
            request.session['user']=username # 将session信息记录到浏览器
            return response
            # set_cookie参数说明：1、user表示写入浏览器的cookie名
            #                    2、username是用户在登录页输入的用户名
            #                    3、3600是设置cookie在浏览器中的保持时间，默认为秒

        else:
            return render(request,'index.html',{'error':'username or password error!'})
#发布会管理
def event_manage(request):
    # username=request.COOKIES.get('user', '') # 读取浏览器cookie
    username=request.session.get('user', '') # 读取浏览器session
    return render(request,'event_manage.html',{'user':username})
'''

# 引用Django认证登录
from django.contrib import auth
from django.contrib.auth.decorators import login_required
#登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        # authenticate函数认证给出的用户名和密码，正确就返回一个user对象否则返回None
        if user is not None:
            auth.login(request,user) # 登录
            request.session['user']=username # 将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return response
            # set_cookie参数说明：1、user表示写入浏览器的cookie名
            #                    2、username是用户在登录页输入的用户名
            #                    3、3600是设置cookie在浏览器中的保持时间，默认为秒

        else:
            return render(request,'index.html',{'error':'username or password error!'})
#发布会管理
@login_required # 限制某个视图函数必须登录才能访问，在函数前加@login_required修饰
def event_manage(request):
    # username=request.COOKIES.get('user', '') # 读取浏览器cookie
    username=request.session.get('user', '') # 读取浏览器session
    return render(request,'event_manage.html',{'user':username})




