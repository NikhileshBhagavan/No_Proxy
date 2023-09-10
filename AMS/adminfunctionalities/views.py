from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import math
from .forms import *
from home.models import *

def addnotice(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.ADDNOTICE(request)
    #if request.method=="GET":
        #form=NoticeForm()
        #return render(request,'addnotice.html',{'form':form})
    #if request.method=="POST":
        #f=NoticeForm(request.POST)
        #f.save()
        #return redirect("/adminlogin/admin/addnotice")

def deletenotice(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.DELETENOTICE(request)
def addstudent(request):
 
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.ADDSTUDENT(request)
def addcourse(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.ADDCOURSE(request)
def addprofessor(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.ADDPROFESSOR(request)
def removestudent(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.REMOVESTUDENT(request)
def removeprofessor(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.REMOVEPROFESSOR(request)
def updatestudentinfo(request,name):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.UPDATESTUDENTINFO(request,name)    
def updateprofessorinfo(request,name):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.UPDATEPROFESSORINFO(request,name)
def reschedulecourse(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.RESCHEDULECOURSE(request)
def initialupdatestudentinfo(request):
    if request.method=='GET':
        q=Student.objects.all()
        return render(request,"initialstudentupdateinfo.html",{'q':q})
    else:
        k=request.POST['studentid']
        if User.objects.filter(username=k,is_staff=False,is_superuser=False).exists():
            return redirect("/adminlogin/admin/updatestudentinfo/"+k)
        else:
            messages.info(request,"Student id not found,please check again")
            return redirect("/adminlogin/admin/initialupdatestudentinfo")
def initialupdateprofessorinfo(request):
    if request.method=="GET":
        q=Professor.objects.all()
        return render(request,"initialprofessorupdate.html",{'q':q})
    else:
        k=request.POST['professorid']
        if User.objects.filter(username=k,is_staff=True,is_superuser=False).exists():
            return redirect("/adminlogin/admin/updateprofessorinfo/"+k)
        else:
            messages.info(request,"Professor id not found,please check again")
            return redirect("/adminlogin/admin/initialupdateprofessorinfo")

def initialtt(request):
    if request.method=="GET":
        f=CourseForm()
        return render(request,"initialtt.html",{'form':f})
    if request.method=="POST":
        a=ADMIN.objects.get(id=request.user.admin.id)
        return a.SHOWTIMETABLE(request,request.POST['branch'],request.POST['semester'])
def managequeries(request):
    if request.method=="GET":
        return render(request,"initialmanagequeries.html")
def queriesfromstudents(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.QUERIESFROMSTUDENTS(request)
def queriesfromstudentsandrespond(request,id):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.QUERIESFROMSTUDENTSANDRESPOND(request,id)
def queriesfromprofessors(request):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.QUERIESFROMPROFESSORS(request)
def queriesfromprofessorsandrespond(request,id):
    a=ADMIN.objects.get(id=request.user.admin.id)
    return a.QUERIESFROMPROFESSORSANDRESPOND(request,id)