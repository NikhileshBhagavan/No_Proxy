from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import math
import os

import face_recognition
from home.models import *
import base64

        
def profile(request):
    
        a=Student.objects.get(id=request.user.student.id)
        return a.VIEWSTUDENTPROFILE(request)
def timetable(request):
        a=Student.objects.get(id=request.user.student.id)
        return a.VIEWTIMETABLE(request)
def queries(request):
        if request.method=="GET":
                semester=request.user.student.semester
                branch=request.user.student.branch
                q=Course.objects.filter(semester=semester,branch=branch)
                li=[]
                for k in q:
                        li.append(k.course_name)
                li=list(set(li))
                return render(request,"stinitialqueries.html",{'li':li})
        if request.method=="POST":
                a=request.POST['to_who']
                if a=="ADMIN":
                        q=Query.objects.filter(send_status=1)
                        return render(request,"responsestudentadmin.html",{'q':q})
                else:
                        l=Course.objects.filter(course_name=request.POST['to_who']).first().query_set.all()
                        q=[]
                        for j in l:
                                if j.from_stu.user.id==request.user.id:
                                        q.append(j)
                                else:
                                        continue
                          


                        return render(request,"courserespondtostudent.html",{'q':q})


def makeaquery(request):
        a=Student.objects.get(id=request.user.student.id)
        return a.MAKEAQUERY(request) 
def markattendance(request):
        a=Student.objects.get(id=request.user.student.id)
        return a.MARKATTENDANCE(request) 
def attended(request):
        messages.info(request,"Profile Found, Your attendance is noted")
        return redirect("/studentlogin/student")
def stats(request):
        s=request.user.student
        li=s.courses.all()
        listofcourses=[]
        for j in li:
                listofcourses.append(j.course_name)
        l=list(set(listofcourses))
        d=dict()
        for j in l:
                prof=Course.objects.filter(course_name=j).first().professor
                d[j]=prof
        return render(request,"studentstats.html",{'l':l,'d':d})
def specificstats(request,coursename):
        a=Student.objects.get(id=request.user.student.id)
        return a.VIEWSTATS(request,coursename)
