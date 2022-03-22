
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path("sigup",views.sigup,name='sigup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
]
