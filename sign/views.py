from django.contrib import admin
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from sign.models import Event,Guest
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
import logging

logger = logging.getLogger(__name__)
"""
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("hello django")
"""
# 首页登录
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
# from django.contrib import auth
# from django.contrib.auth.decorators import login_required
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
# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response
'''
#发布会管理
@login_required # 限制某个视图函数必须登录才能访问，在函数前加@login_required修饰
def event_manage(request):
    # username=request.COOKIES.get('user', '') # 读取浏览器cookie
    username=request.session.get('user', '') # 读取浏览器session
    return render(request,'event_manage.html',{'user':username})
'''
#发布会管理
# 导入Event类，通过Event.objects.all()查询所有发布会对象，通过render方法附加在event_manage.html并返回给客户端
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username=request.session.get('user', '') # 读取浏览器session
    return render(request,'event_manage.html',{'user':username,
                                               'events':event_list})
# 发布会搜素
@login_required
def search_name(request):
    username = request.session.get('username', '')
    search_name = request.GET.get("name", "")
    # search_name_bytes = search_name.encode(encoding="utf-8")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})
# 嘉宾管理
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 嘉宾手机号的查询
@login_required
def search_phone(request):
    username = request.session.get('username', '')
    search_phone = request.GET.get("phone", "")
    # search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_phone)

    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "guest_manage.html", {"user": username,
                                                   "guests": contacts,
                                                   "phone":search_phone})


# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    # guest_list = Guest.objects.filter(event_id=eid)           # 签到人数
    # sign_list = Guest.objects.filter(sign="1", event_id=eid)   # 已签到数
    # guest_data = str(len(guest_list))
    # sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,
                                               # 'guest':guest_data,
                                               # 'sign':sign_data
                                               }
                  )


# 前端签到页面
def sign_index2(request,event_id):
    event_name = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index2.html',{'eventId': event_id,
                                               'eventNanme': event_name})


# 签到动作
@login_required
def sign_index_action(request,eid):

    event = get_object_or_404(Event, id=eid)
    # guest_list = Guest.objects.filter(event_id=event_id)
    # guest_data = str(len(guest_list))
    # sign_data = 0   #计算发布会“已签到”的数量
    # for guest in guest_list:
    #     if guest.sign == True:
    #         sign_data += 1

    phone = request.POST.get('phone','')
    print(phone)

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.',
                                                   # 'guest':guest_data,
                                                   # 'sign':sign_data
                                                   })

    result = Guest.objects.filter(phone = phone,event_id = eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.',
                                                   # 'guest':guest_data,'sign':sign_data
                                                   })

    result = Guest.objects.get(event_id = eid,phone = phone)

    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has sign in.",
                                                   # 'guest':guest_data,
                                                   # 'sign':sign_data
                                                   })
    else:
        Guest.objects.filter(event_id = eid,phone = phone).update(sign = '1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint':'sign in success!',
                                                   'user': result,
                                                   # 'guest':guest_data,
                                                   # 'sign':str(int(sign_data)+1)
                                                   })
