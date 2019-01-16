"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from sign import views #导入sign应用的views文件

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'index/',views.index),#添加index路径
    path(r'login_action/', views.login_action),
    path(r'event_manage/', views.event_manage),
    path(r'accounts/login/', views.index),
    path(r'', views.index),
    path(r'search_name/', views.search_name),
    path(r'guest_manage/', views.guest_manage),
    path(r'search_phone/', views.search_phone),
    path(r'sign_index/<eid>/', views.sign_index),
    path(r'sign_index2/<eid>/', views.sign_index2),
    path(r'sign_index_action/<eid>/', views.sign_index_action),
    path(r'api/', include('sign.urls', namespace="sign")),
    path(r'logout/', views.logout)
]
