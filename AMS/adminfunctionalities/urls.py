from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('addnotice',views.addnotice,name="addnotice"),
    path('deletenotice',views.deletenotice,name="deletenotice"),
    path('addstudent',views.addstudent,name="addstudent"),
    path('addcourse',views.addcourse,name="addcourse"),
    path('managequeries',views.managequeries,name="managequeries"),
    path('queriesfromstudents',views.queriesfromstudents,name="queriesfromstudents"),
    path('queriesfromstudents/<int:id>',views.queriesfromstudentsandrespond,name="queriesfromstudentsandrespond"),
    path('queriesfromprofessors/<int:id>',views.queriesfromprofessorsandrespond,name="queriesfromprofessorsandrespond"),
    path('queriesfromprofessors',views.queriesfromprofessors,name="queriesfromprofessors"),
    path('addcourse/initialtt',views.initialtt,name="initialtt"),
    path('addprofessor',views.addprofessor,name="addprofessor"),
    path('removestudent',views.removestudent,name="removestudent"),
    path('removeprofessor',views.removeprofessor,name="removeprofessor"),
    path('updatestudentinfo/<str:name>',views.updatestudentinfo,name="updatestudentinfo"),
    path('updateprofessorinfo/<str:name>',views.updateprofessorinfo,name="updateprofessorinfo"),
    path('updateprofessorinfo',views.updateprofessorinfo,name="updateprofessorinfo"),
    path('reschedulecourse',views.reschedulecourse,name="reschedulecourse"),
    path('initialupdatestudentinfo',views.initialupdatestudentinfo,name='initialupdatestudentinfo'),
    path('initialupdateprofessorinfo',views.initialupdateprofessorinfo,name="initialupdateprofessorinfo")



]