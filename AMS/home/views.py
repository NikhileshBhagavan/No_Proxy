from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
import math
from .models import *
from django.db.models import Count, F, Value
import datetime 
# Create your views here.

def homepage(request):
   

    if(request.method=='GET'):
        if ADMIN.objects.all().count()==User.objects.filter(is_staff=Tis_superuser=Truerue,).count():
            print("hello")
        else:
            if User.objects.filter(is_staff=True,is_superuser=True).exists():
                for i in User.objects.filter(is_staff=True,is_superuser=True):
                    try:
                        print(i.admin)
                    except:
                        a=ADMIN(admin_user=i)
                        a.save()
                    print(i.admin)

                    
                        
        #if not Absentdates.objects.filter(dates_of_absent=datetime.date.today()).exists():

         #   a=Absentdates()
        
        
          #  day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
           # da = datetime.date.today().weekday()
           # print(day_name[da])
           # a.day=day_name[da]
            #a.save()
        return render(request,'sams.html')
def nots(request):
    if(request.method=='GET'):
        objs=notices.objects.all()
       
        return render(request,'announcements.html',{'objs':objs})
def contact(request):
    if(request.method=='GET'):
        return render(request,'contactus.html')
def studentlogin(request):
    if(request.method=='GET'):
        return render(request,'studentlogin.html')
    if(request.method=='POST'):
        
        username=request.POST['your_name']
        password=request.POST['your_pass']
        objo=auth.authenticate(username=username,password=password)
        print(request.user.is_authenticated)
        # returns user object if present
        if objo is not None:
            auth.login(request,objo)
            
            if objo.is_superuser==False and objo.is_staff==False:
                
                return redirect("/studentlogin/student")
            else:
                auth.logout(request)
                messages.info(request,"Student details not found or Access denied")
                return redirect("/studentlogin")
        else:
            messages.info(request,"STUDENT NOT FOUND ,PLEASE CHECK YOUR USERNAME AND PASSWORD AGAIN")
            return redirect("/studentlogin")
def sthome(request):
    if(request.method=='GET'):
        return render(request,'stproj.html')
def stlogout(request):
    auth.logout(request)
    
    return redirect("/")
def stafflogin(request):
    if(request.method=='GET'):
        return render(request,'stafflogin.html')
    if request.method=="POST":
        username=request.POST['your_name']
        password=request.POST['your_pass']
        objo=auth.authenticate(username=username,password=password,is_superuser=False,is_staff=True)
        print(request.user.is_authenticated)
        # returns user object if present
        if objo is not None:
            auth.login(request,objo)
            if objo.is_staff==True and objo.is_superuser==False:
                return redirect("/stafflogin/staff")
            else:
                auth.logout(request)
                messages.info(request,"Staff details not found or access denied")
                return redirect("/stafflogin")
        else:
            messages.info(request,"Staff NOT FOUND ,PLEASE CHECK YOUR USERNAME AND PASSWORD AGAIN")
            return redirect("/stafflogin")
def staffhome(request):
    if request.method=='GET':
        return render(request,'staffproj.html')
def stafflogout(request):
    auth.logout(request)
    
    return redirect("/")
def adminlogin(request):
    if(request.method=='GET'):
      
        return render(request,'adminlogin.html')
    if(request.method=='POST'):
        username=request.POST['admin_username']
        password=request.POST['admin_password']
        objo=auth.authenticate(username=username,password=password)
        print(request.user.is_authenticated)
        # returns user object if present
        if objo is not None:
            auth.login(request,objo)
            if objo.is_superuser==True:
                return redirect("/adminlogin/admin")
            else:
                auth.logout(request)
                messages.info(request,"Admin details not found or access denied")
                return redirect('/adminlogin')
        else:
            messages.info(request,"ADMIN NOT FOUND ,PLEASE CHECK YOUR USERNAME AND PASSWORD AGAIN")
            return redirect("/adminlogin")
def adlog(request):
    if(request.method=='GET'):
        return render(request,'proj.html')
def checkout(request):
    auth.logout(request)
    
    return redirect("/")


def GENERATEOTP():
    s="0123456789"
    b=""
    for i in range(8):
        b=b+s[int(random.random()*10)]
    return b
def forgotpassword(request):
    if request.method=='GET':
        return render(request,"forgotpassword.html")
    if request.method=='POST':
        username=request.POST["username"]
        email=request.POST["email"]
        if User.objects.filter(username=username,email=email).exists():
            obj=User.objects.get(username=username,email=email)
            print("I m dead")
            subject = 'Donot reply'
            otp=GENERATEOTP()
            name=obj.username
            message = 'Hi'+name+"YOUR OTP TO SET NEW PASSWORD IS "+otp
            recipient_list = [obj.email]
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject,message, email_from, recipient_list )
            print("i am here")
            if Password.objects.filter(passwordchangerid=obj.id).exists():
                p=Password.objects.get(passwordchangerid=obj.id)
                p.passwordchangerotp=otp
                p.save()
                print(p)
            else:
                p=Password(passwordchangerid=obj.id,passwordchangerotp=otp)
                p.save()

            return redirect("/forgotpassword/confirm/"+str(obj.id))
        else:
            messages.info(request,"USERNAME AND EMAIL ARE NOT MATCHING OR NOT FOUND")
            return redirect("/forgotpassword")

def lemmecheck(request,passwordchangerid):
    if request.method=="GET":
        
        return render(request,"confirm.html")
    if request.method=="POST":
        
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if Password.objects.get(passwordchangerid=int(passwordchangerid)).passwordchangerotp==request.POST["OTP"]:
                u=User.objects.get(id=int(passwordchangerid))
                u.set_password(password1)
                u.save()
                p=Password.objects.get(passwordchangerid=int(passwordchangerid))
                p.passwordchangerotp=''
                p.save()

                messages.info(request,"password changed successfully")
                return redirect("/")
            else:
                messages.info(request,"OTP's not matching,check again")
                return redirect("/forgotpassword/confirm/"+passwordchangerid)
        else:
            messages.info(request,"PASSWORD's not matching")
            return redirect("/forgotpassword/confirm/"+passwordchangerid)

