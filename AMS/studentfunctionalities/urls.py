from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('profile',views.profile,name="profile"),
    path('timetable',views.timetable,name="timetable"),
    path('queries',views.queries,name="queries"),
    path('makeaquery',views.makeaquery,name="makeaquery"),
    path('markattendance',views.markattendance,name="markattendance"),
    path('attended',views.attended,name="attended"),
    path('stats',views.stats,name="stats"),
    path('stats/<str:coursename>',views.specificstats,name="specificstats")
    
  
    



]
