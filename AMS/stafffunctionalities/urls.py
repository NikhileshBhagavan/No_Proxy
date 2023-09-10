from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('profile',views.profile,name="profile"),
    path('timetable',views.timetable,name="timetable"),
    path('staffqueries',views.staffqueries,name="staffqueries"),
    path('staffmakeaquery',views.staffmakeaquery,name="staffmakeaquery"),
    path('staffmanagequeries',views.staffmanagequeries,name="staffmanagequeries"),
    path('staffmanagequeries/<int:id>',views.responsestudentcourse,name="responsestudentcourse"),
    path('takeattendance',views.takeattendance,name="takeattendance"),
    path('stoptakingattendance',views.stoptakingattendance,name="stoptakingattendance"),
    path('studentattendance',views.studentattendance,name="studentattendance"),
    path('studentattendance/<str:coursename>',views.staffstudentstats,name="staffstudentstats"),
    path('studentattendance/<str:coursename>/<str:name>',views.staffspecificstudentstats,name="staffspecificstudentstats"),
    path('studentattendance/<str:coursename>/<str:name>/sendwarning',views.sendwarning,name="sendwarning"),
    path('studentattendance/<str:coursename>/<str:name>/modifyattendance',views.modifyattendance,name="modifyattendance"),
    path('studentattendance/<str:coursename>/<str:name>/addattendance',views.addattendance,name="addattendance"),
    path('studentattendance/<str:coursename>/<str:name>/deleteattendance',views.deleteattendance,name="deleteattendance")

    

    



]
