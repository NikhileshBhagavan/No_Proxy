from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import send_mail
import random
import math
from datetime import date
from home.models import *
from stafffunctionalities.forms import ModifyForm

def GENERATEPASSWORD():
            s="0123456789"
            b=""
            for i in range(8):
                b=b+s[int(random.random()*10)]
            print(b)
            return b
def profile(request):
    
        a=Professor.objects.get(id=request.user.professor.id)
        return a.VIEWSTAFFPROFILE(request)
def timetable(request):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.VIEWTIMETABLE(request)
def staffqueries(request):
        if request.method=="GET":
                
                return render(request,"staffinitialqueries.html")
        if request.method=="POST":
                a=request.POST['to_who']
                if a=="ADMIN":
                        q=Query.objects.filter(send_status=2)
                        return render(request,"responsestaffadmin.html",{'q':q})
                else:
                        pass
def staffmakeaquery(request):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.STAFFMAKEAQUERY(request)
def staffmanagequeries(request):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.STAFFMANAGEQUERIES(request)
def responsestudentcourse(request,id):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.RESPONSESTUDENTCOURSE(request,id)
def takeattendance(request):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.TAKEATTENDANCE(request)

def stoptakingattendance(request):
        if request.method=="POST":
                a=Professor.objects.get(id=request.user.professor.id) 
                x=a.course_set.filter(attendance_taking_status=True).first()
                name=x.course_name
                print(name)
                li=x.attendance_set.filter(attended_status=False)
                liofstuabs=[]

                for z in li:
                        liofstuabs.append(z.stud)
                dt=date.today()
                day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
                da = dt.weekday()
          
                print(li,"hello")
                for b in li:

                        if not b.absentdates.filter(dates_of_absent__day=dt.day,dates_of_absent__month=dt.month,dates_of_absent__year=dt.year,attendanceid=b.id).exists():
                                y=Absentdates.objects.create(dates_of_absent=dt,day=day_name[da],attendanceid=b.id,no_of_classes_absent=1)
                                y.save()
                                b.absentdates.add(y)
                                b.save()
                        else:
                                t=b.absentdates.get(dates_of_absent__day=dt.day,dates_of_absent__month=dt.month,dates_of_absent__year=dt.year,attendanceid=b.id)  
                                t.no_of_classes_absent=t.no_of_classes_absent+1
                                t.save()
                                
                
                print(liofstuabs,"bye")
                print(li)

                for j in x.attendance_set.all():
                       j.attended_status=False
                       j.code=''
                       j.save()
                print(li)
                for k in a.course_set.filter(attendance_taking_status=True):
                        k.attendance_taking_status=False
                        k.save()
                print(name)
                return render(request,"showlist.html",{'li':liofstuabs,'name':name})
def studentattendance(request):
        if request.method=="GET":
                a=Professor.objects.get(id=request.user.professor.id)
                q=a.course_set.all()
                li=[]
                for j in q:
                        li.append(j.course_name)
                li=list(set(li))

                return render(request,"studentattendance.html",{'li':li})
def staffstudentstats(request,coursename):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.VIEWSTUDENTSTATS(request,coursename)
def staffspecificstudentstats(request,coursename,name):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.VIEWSPECIFICSTUDENTSTATS(request,coursename,name)
def sendwarning(request,coursename,name):
        a=Professor.objects.get(id=request.user.professor.id)
        return a.SENDWARNING(request,coursename,name)
def modifyattendance(request,coursename,name):
       
        print(coursename)
        print(name)
        return render(request,"modifyattendance.html",{'coursename':coursename,'name':name})
def addattendance(request,coursename,name):
        if request.POST['modifydate']=='':
                messages.info(request,"Please select date")
                return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")
        else:
                a=Course.objects.filter(course_name=coursename).first().attendance_set.all()
                obj=None
                for k in a:
                        if k.stud.user.username==name:
                                obj=k
                                break
                print(obj)
                s=request.POST['modifydate']
                dt=date(int(s[0:4]),int(s[5:7]),int(s[8:]))
                print(dt)
                if obj.attended_classes_count==obj.total_classes_count:
                        messages.info(request,"Seriously,attendance is already 100%")
                        return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")
                
                if obj.absentdates.filter(dates_of_absent=dt).exists():
                        obj.attended_classes_count=obj.attended_classes_count+1
                        obj.save()
                        a=obj.absentdates.get(dates_of_absent=dt)
                        if a.no_of_classes_absent<=1:
                                a.delete()
                        else:
                                a.no_of_classes_absent=a.no_of_classes_absent-1
                                a.save()
                        messages.info(request,"attendance modified successfully")
                        return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")
                else:   
                        print(type(request.POST['modifydate']))
                        print(request.POST['modifydate'])
                        obj.attended_classes_count=obj.attended_classes_count+1
                        obj.save()
                        messages.info(request,"attendance modified successfully")
                        return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")
def deleteattendance(request,coursename,name):
        if request.POST['modifydate']=='':
                messages.info(request,"Please select date")
                return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")
        else:
                a=Course.objects.filter(course_name=coursename).first().attendance_set.all()
                obj=None
                for k in a:
                        if k.stud.user.username==name:
                                obj=k
                                break
                s=request.POST['modifydate']
                dt=date(int(s[0:4]),int(s[5:7]),int(s[8:]))
                print(dt)
                if obj.attended_classes_count==0:
                        messages.info(request,"seriously,attendance is already 0%")
                        return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")
                
                if obj.absentdates.filter(dates_of_absent=dt).exists():
                        obj.attended_classes_count=obj.attended_classes_count-1
                        obj.save()
                        a=obj.absentdates.get(dates_of_absent=dt)
                       
                        a.no_of_classes_absent=a.no_of_classes_absent+1
                        a.save()
                        messages.info(request,"attendance modified successfully")
                        return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")
                else:
                        s=request.POST['modifydate']
                        dt=date(int(s[0:4]),int(s[5:7]),int(s[8:]))
                        print(dt)
                        day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
                        da = dt.weekday()
                        a=Absentdates(dates_of_absent=dt,no_of_classes_absent=1,attendanceid=obj.id,day=day_name[da])
                        a.save()
                        obj.attended_classes_count=obj.attended_classes_count-1
                        obj.save()
                        obj.absentdates.add(a)
                        obj.save()
                        messages.info(request,"attendance modified successfully")
                        return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name+"/modifyattendance")