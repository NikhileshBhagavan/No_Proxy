from django.db import models
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.db.models.deletion import SET_NULL
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse,HttpResponse
import face_recognition
import random
import os
import os
from shutil import *
from pathlib import Path
import base64

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from django.db.models.fields import DateField, IntegerField
from django.http.response import HttpResponse

from django.shortcuts import render,redirect
# Create your models here.
# Create your models here. 

def faculty_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.user.username
    filename = name +'.'+ ext 
    return 'Faculty_Images/{}'.format(filename)

def student_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.user.username 
    filename = name +'.'+ ext 
    return 'Student_Images/{}/{}/{}'.format(instance.semester,instance.branch,filename)

class Password(models.Model):
    passwordchangerid=models.IntegerField(null=True,blank=True)
    passwordchangerotp=models.CharField(max_length=100,null=True,blank=True)

class Absentdates(models.Model):
    dates_of_absent=models.DateField(auto_now_add=False,auto_now=False,null=True,blank=True)
    day=models.CharField(max_length=100,blank=True,null=True)
    no_of_classes_absent=models.IntegerField(default=0,null=True,blank=True)
    attendanceid=models.IntegerField(blank=True,null=True)

class Attendance(models.Model):
    attended_classes_count=models.IntegerField(blank=True,null=True)
    total_classes_count=models.IntegerField(blank=True,null=True)
    
    attended_status=models.BooleanField(default=False)
    code=models.CharField(max_length=200,null=True,blank=True)
    absentdates=models.ManyToManyField(Absentdates)
    stud=models.ForeignKey("Student",on_delete=models.CASCADE,null=True)
    cour=models.ManyToManyField("Course")
    limits=models.IntegerField(default=2)

class Query(models.Model):
    question=models.TextField(null=True,blank=True)
    answer=models.TextField(blank=True,null=True)
    answered_status=models.BooleanField(default=False)
    send_status=models.IntegerField(blank=False,null=False)
    from_stu=models.ForeignKey("Student",on_delete=models.CASCADE,null=True)
    to_adm=models.ForeignKey("ADMIN",on_delete=models.CASCADE,null=True)
    to_course=models.ManyToManyField("Course")
    from_prof=models.ForeignKey("Professor",on_delete=models.CASCADE,null=True)
    #0-from student to course
    #1-from student to admin
    #2-from prof to admin
class notices(models.Model):
    Notice=models.TextField(null=True,blank=True)
from .forms import *
class Professor(models.Model):
    profprofilepic=models.FileField(upload_to=faculty_directory_path,null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    spamprofilepic=models.FileField(upload_to="spam_faculty_images/",null=True,blank=True)

    def SENDWARNING(self,request,coursename,name):
        q=Course.objects.filter(course_name=coursename).first().attendance_set.all()
        u=User.objects.get(username=name)
       
        obj=None
        for k in q:
            if k.stud.user.username==name:
                obj=k
                break
        percentage=int((obj.attended_classes_count/obj.total_classes_count)*100)
        
        li=obj.absentdates.all()
        s=''
        for k in li:
            s=s+str(k.dates_of_absent)+'('+k.day+")"+'(No of classes absent on that day: '+str(k.no_of_classes_absent)+")"+','
        subject = 'ATTENDANCE WARNING FOR '+coursename
                            
                          
        message = 'Hi'+name +" YOUR ATTENDANCE PERCENTAGE FOR COURSE "+coursename + str(percentage)+"This is warning that you attendance is less than 80%"+ " continues,your marks may be cutdown"+'Your absent days are '+s+"  please attend classes regularly"
        
       
        recipient_list = [u.email]
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject,message, email_from, recipient_list )
        messages.info(request,"warning sent successfully")
        return redirect("/stafflogin/staff/studentattendance/"+coursename+'/'+name)
           
                            


    
    def VIEWSTAFFPROFILE(self,request):
        if request.method=="GET":

            s=Professor.objects.get(id=request.user.professor.id)
            q=s.course_set.all()
            li=[]
            for k in q:
                li.append(k.course_name)
            li=list(set(li))
            print(s.spamprofilepic.url)
            return render(request,"staffprofile.html",{'s':s,'li':li})
        if request.method=="POST":
            a=request.user.email
            if User.objects.filter(email=request.POST['email']).exists() and a!=request.POST['email']:
                messages.info(request,"email already taken")
                return redirect("/stafflogin/staff/profile")
            else:
                first_name=request.POST['firstname']
                last_name=request.POST['lastname']
                if len(request.FILES)>0:
                    #s='Faculty_Images/{}'.format(request.user.username)
                    #path=os.path.join(BASE_DIR,"media/"+s)
                    #if os.path.isfile(path+'.png'):
                        #os.remove(path+".png")
                    #if os.path.isfile(path+'.jpeg'):
                       # os.remove(path+".jpeg")
                    #if os.path.isfile(path+'.jpg'):
                       # os.remove(path+".jpg")
                   
                    spamprofilepic=request.FILES['profprofilepic']
                    s=Professor.objects.get(id=request.user.professor.id)
                    s.user.first_name=first_name
                    s.user.last_name=last_name
                    s.user.email=request.POST['email']
                    s.user.save()
                    s.spamprofilepic=spamprofilepic
                    s.save()
                    messages.info(request,"updatedsuccessfully")
                    return redirect("/stafflogin/staff/profile")
                else:
                    s=Professor.objects.get(id=request.user.professor.id)
                    s.user.first_name=first_name
                    s.user.last_name=last_name
                    s.user.email=request.POST['email']
                    s.user.save()
               
                    s.save()
                    messages.info(request,"updatedsuccessfully")
                    return redirect("/stafflogin/staff/profile")
          
    
    def VIEWTIMETABLE(self,request):
        if request.method=="GET":
            obj=Professor.objects.get(id=request.user.professor.id)
            q=obj.course_set.all()
            monday=dict()
            tuesday=dict()
            wednesday=dict()
            thursday=dict()
            friday=dict()
           
            t=[monday,tuesday,wednesday,thursday,friday]
            for k in q:
                if k.day=="MONDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in monday:
                        
                        monday[k.time]=li
                    else:
                        monday[k.time]=monday[k.time]+li
                if k.day=="TUESDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in tuesday:
                        
                        tuesday[k.time]=li
                    else:
                        tuesday[k.time]=tuesday[k.time]+li
                if k.day=="WEDNESDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in wednesday:
                        
                        wednesday[k.time]=li
                    else:
                        wednesday[k.time]=wednesday[k.time]+li
                if k.day=="THURSDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in thursday:
                        
                        thursday[k.time]=li
                    else:
                        thursday[k.time]=thursday[k.time]+li
                if k.day=="FRIDAY":
                    li=[[k.course_name,k.branch,k.semester]]
                    if k.time not in friday:
                        
                        friday[k.time]=li
                    else:
                        friday[k.time]=friday[k.time]+li
            di={'h':10}
            for i in t:
                if "10:00-11:00" not in i:
                    i["a"]=[]
                else:
                    p=i["10:00-11:00"]
                    del i["10:00-11:00"]
                    i["a"]=p
                if "11:00-12:00" not in i:
                    i["b"]=[]
                else:
                    p=i["11:00-12:00"]
                    del i["11:00-12:00"]
                    i["b"]=p
                if "14:00-15:00" not in i:
                    i["c"]=[]
                else:
                    p=i["14:00-15:00"]
                    del i["14:00-15:00"]
                    i["c"]=p
                if "15:00-16:00" not in i:
                    i["d"]=[]
                else:
                    p=i["15:00-16:00"]
                    del i["15:00-16:00"]
                    i["d"]=p
            
            print(monday)
            return render(request,"viewstafftimetable.html",{'obj':obj,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday})
    def STAFFMAKEAQUERY(self,request):
        if request.method=="GET":
            
            form=QueryFormRequest()
            return render(request,"staffmakeaquery.html",{'form':form})
        if request.method=="POST":
            if request.POST['question']=="":
                messages.info(request,"please fill something before submitting")
                return redirect("/stafflogin/staff/staffmakeaquery")
            else:
                to_who=request.POST['to_who']
                if to_who=="ADMIN":
                    question=request.POST['question']
                    send_status=2
                    from_prof=Professor.objects.get(id=request.user.professor.id)
                    to_adm=ADMIN.objects.all().first()
                    query=Query(question=question,send_status=send_status,from_prof=from_prof,to_adm=to_adm)
                    query.save()
                    messages.info(request,"query submitted successfully")
                    return redirect("/stafflogin/staff/staffqueries")
    def STAFFMANAGEQUERIES(self,request):
        if request.method=="GET":
            a=Professor.objects.get(id=request.user.professor.id)
            q=a.course_set.all()
            li=[]
            for i in q:
                li.append(i.course_name)
            li=list(set(li))
            d=dict()
            for j in li:
                l=list(Course.objects.filter(course_name=j).first().query_set.filter(answered_status=False))
                d[j]=l
            return render(request,"staffmanagequeries.html",{'d':d})
    def RESPONSESTUDENTCOURSE(self,request,id):
        if request.method=="GET":
            ki=Query.objects.get(id=id,answered_status=False)
            print(ki)
            question=ki.question
            f=QueryFormResponse()
            return render(request,"responsestudentcourse.html",{'ki':ki,'form':f})
        if request.method=="POST":
                if request.POST['answer']=="":
                    messages.info(request,"please respond")
                    return redirect("/stafflogin/staff/staffmanagequeries/"+str(id))
                else:
                    q=Query.objects.get(id=id)
                    q.answered_status=True
                    q.answer=request.POST['answer']
                    q.save()
                    messages.info(request,"response submitted")
                    return redirect("/stafflogin/staff/staffmanagequeries")
    def VIEWSTUDENTSTATS(self,request,coursename):
        att=Course.objects.filter(course_name=coursename).first().attendance_set.all()
        classesattended=0
        totalclasses=0
        for a in att:
            classesattended=classesattended+a.attended_classes_count
            totalclasses=totalclasses+a.total_classes_count
        
            totalclassaverage=int((classesattended/totalclasses)*100)
        li=dict()
        for k in att:
            percentage=int((k.attended_classes_count/k.total_classes_count)*100)
            li[k]=percentage
       
        print(li)
       

        
        return render(request,"studentstaffstats.html",{'li':li,'att':att,'classavg':totalclassaverage,'coursename':coursename})
    def VIEWSPECIFICSTUDENTSTATS(self,request,coursename,name):
        q=Course.objects.filter(course_name=coursename).first().attendance_set.all()
        classesattended=0
        totalclasses=0
        for a in q:
            classesattended=classesattended+a.attended_classes_count
            totalclasses=totalclasses+a.total_classes_count
        totalclassaverage=int((classesattended/totalclasses)*100)
        obj=None
        for k in q:
            if k.stud.user.username==name:
                obj=k
                break
        percentage=int((obj.attended_classes_count/obj.total_classes_count)*100)
        li=obj.absentdates.all()
        print(li)
        student=User.objects.get(username=name).student
        return render(request,"specificstudentstaff.html",{'obj':obj,'percentage':percentage,'li':li,'coursename':coursename,'student':student,'classavg':totalclassaverage})
    def GENERATEPASSWORD(self):
            s="0123456789"
            b=""
            for i in range(8):
                b=b+s[int(random.random()*10)]
            print(b)
            return b
    def TAKEATTENDANCE(self,request):
        if request.method=="GET":
                a=Professor.objects.get(id=request.user.professor.id)
                q=a.course_set.all()
                li=[]
                for j in q:
                        li.append(j.course_name)
                li=list(set(li))
                b=False
                x=None
                if a.course_set.filter(attendance_taking_status=True).exists():
                        x=a.course_set.filter(attendance_taking_status=True).first().course_name
                        #t=a.course_set.filter(attendance_taking_status=True).first().attendance_set.all()
                        #for j in t:
                        #       j.total_classes_count=j.total_classes_count+1
                        #       j.save()
                        b=True
        
                return render(request,'takeattendance.html',{'li':li,'x':x,'b':b})
        if request.method=="POST":
                a=Professor.objects.get(id=request.user.professor.id)
                print(request.POST['course'])
                q=Course.objects.filter(course_name=request.POST['course'])
                print(q)
                for j in q:
                        j.attendance_taking_status=True
                        j.save()
                k=Course.objects.filter(course_name=request.POST['course']).first().attendance_set.all()
                for m in k:
                        m.total_classes_count=m.total_classes_count+1
                        code=a.GENERATEPASSWORD()
                        m.code=code
                        m.save()
                            
                        #subject = 'Do not reply'
                            
                          
                        #message = 'Hi '+m.stud.user.username+"   YOUR CODE FOR TAKING ATTENDACE FOR COURSE" +request.POST['course']+ "IS    "+code
                        #recipient_list = [m.stud.user.email]
                        #email_from = settings.EMAIL_HOST_USER
                        #send_mail(subject,message, email_from, recipient_list )

                
                return HttpResponse("taking attendance")

                
         
class Course(models.Model):
    COURSE_NAME=[
        ('CSN221','CSN221'),
        ('CSN291','CSN291'),
        ('PHN005','PHN005'),
        ('MAN005','MAN005'),
        ('CEN105','CEN105')
    ]
    COURSE_BRANCH=[
        ('CSE','CSE'),
        ('ECE','ECE'),
        ('EE','EE'),
        ('ME','ME')
    ]
    COURSE_SEMESTER=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8')
    ]
    COURSE_TEACHING_DAY=[
        ('MONDAY','MONDAY'),
        ('TUESDAY','TUESDAY'),
        ('WEDNESDAY','WEDNESDAY'),
        ('THURSDAY','THURSDAY'),
        ('FRIDAY','FRIDAY')
    ]
    COURSE_TEACHING_TIME=[
        ('10:00-11:00','10:00-11:00'),
        ('11:00-12:00','11:00-12:00'),
        ('14:00-15:00','14:00-15:00'),
        ('15:00-16:00','15:00-16:00'),

    ]
    attendance_taking_status=models.BooleanField(default=False)
    professor=models.ForeignKey(Professor,on_delete=SET_NULL,null=True)
    course_syllabus=models.TextField(blank=False)
    course_name = models.CharField(
        max_length=10,
        choices=COURSE_NAME,
        default='1'
    )
    branch=models.CharField(
        max_length=10,
        choices=COURSE_BRANCH,
        default='CSE'
    )
    semester = models.CharField(
        max_length=10,
        choices=COURSE_SEMESTER,
        default='1'
    )
    day=models.CharField(
        max_length=20,
        choices=COURSE_TEACHING_DAY ,
        default='MONDAY'
    )
    time=models.CharField(
        max_length=20,
        choices=COURSE_TEACHING_TIME ,
        default='10:00-11:00'
    )



class Student(models.Model):
    SEMESTER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8')
          

    ]
    BRANCH_CHOICES=[
        ('CSE','CSE'),
        ('ECE','ECE'),
        ('EE','EE'),
        ('ME','ME')
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    spamprofilepic=models.FileField(upload_to="spam_student_images/",null=True,blank=True)
    semester = models.CharField(
        max_length=2,
        choices=SEMESTER_CHOICES,
        default='1'
    )
    branch=models.CharField(
        max_length=5,
        choices=BRANCH_CHOICES,
        default='CSE'
    )
    courses=models.ManyToManyField(Course)
    studprofilepic=models.FileField(upload_to=student_directory_path,null=True,blank=True)
    
    
   

    def VIEWSTUDENTPROFILE(self,request):
        if request.method=="GET":
            s=Student.objects.get(id=request.user.student.id)
            print(s.spamprofilepic.url)
            return render(request,"studentprofile.html",{'s':s})
        if request.method=="POST":
            a=request.user.email
            if User.objects.filter(email=request.POST['email']).exists() and a!=request.POST['email']:
                messages.info(request,"email already taken")
                return redirect("/studentlogin/student/profile")
            else:
                first_name=request.POST['firstname']
                last_name=request.POST['lastname']
                if len(request.FILES)>0:
                    #unknown_image=face_recognition.load_image_file(request.FILES['studprofilepic'])
                    #unknown_face_encoding = face_recognition.face_encodings(unknown_image)
                     #if len(unknown_face_encoding) <=0 :
           
                     #    messages.info(request,"No face found,please fill again")
                      #   return redirect("/studentlogin/student/profile")
                     #else:
                        
                        
                        
                         #p='Student_Images/{}/{}/{}'.format(request.user.student.semester,request.user.student.branch,request.user.username)
                         #path=os.path.join(BASE_DIR,"media/"+p)
                         #if os.path.isfile(path+'.png'):
                         #    os.remove(path+".png")
                         #if os.path.isfile(path+'.jpeg'):
                         #    os.remove(path+".jpeg")
                         # os.path.isfile(path+'.jpg'):
                          #   os.remove(path+".jpg")
                         #print(os.path.isfile(path+'.png'))
                    student=request.user.student
                    #t=student.find(request,request.FILES['studprofilepic'])
                        #print(t)
                        #if t=="USERNOTFOUND":
                    spamprofilepic=request.FILES['studprofilepic']
                    s=Student.objects.get(id=request.user.student.id)
                    s.user.first_name=first_name
                    s.user.last_name=last_name
                    s.user.email=request.POST['email']
                    s.user.save()
                    s.spamprofilepic=spamprofilepic
                    s.save()
                    messages.info(request,"updatedsuccessfully")
                    return redirect("/studentlogin/student/profile")
                        #else:
                         #   messages.info(request,"another person using account,please try again to update")
                         #   return redirect("/studentlogin/student/profile")
                else:
                    s=Student.objects.get(id=request.user.student.id)
                    s.user.first_name=first_name
                    s.user.last_name=last_name
                    s.user.email=request.POST['email']
                    s.user.save()
               
                    s.save()
                    messages.info(request,"updatedsuccessfully")
                    return redirect("/studentlogin/student/profile")
            
    def VIEWTIMETABLE(self,request):
        if request.method=="GET":
            branch=request.user.student.branch
            semester=request.user.student.semester
            a=Course.objects.filter(branch=branch,semester=semester)
            monday=dict()
            tuesday=dict()
            wednesday=dict()
            thursday=dict()
            friday=dict()
            br=branch
            sem=semester
            li=[monday,tuesday,wednesday,thursday,friday]
            for k in a:
                if k.day=="MONDAY":
                    monday[k.time]=k.course_name
                if k.day=="TUESDAY":
                    tuesday[k.time]=k.course_name
                if k.day=="WEDNESDAY":
                    wednesday[k.time]=k.course_name
                if k.day=="THURSDAY":
                    thursday[k.time]=k.course_name
                if k.day=="FRIDAY":
                    friday[k.time]=k.course_name
            di={'h':10}
            for i in li:
                if "10:00-11:00" not in i:
                    i["a"]="-"
                else:
                    p=i["10:00-11:00"]
                    del i["10:00-11:00"]
                    i["a"]=p
                if "11:00-12:00" not in i:
                    i["b"]="-"
                else:
                    p=i["11:00-12:00"]
                    del i["11:00-12:00"]
                    i["b"]=p
                if "14:00-15:00" not in i:
                    i["c"]="-"
                else:
                    p=i["14:00-15:00"]
                    del i["14:00-15:00"]
                    i["c"]=p
                if "15:00-16:00" not in i:
                    i["d"]="-"
                else:
                    p=i["15:00-16:00"]
                    del i["15:00-16:00"]
                    i["d"]=p
            
            print(monday)
            #return render(request,"spotstimetable.html",{'branch':br,'semester':sem,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'di':di})
            return render(request,"viewstudenttimetable.html",{'branch':br,'semester':sem,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'di':di})
    def MAKEAQUERY(self,request):
        if request.method=="GET":
            semester=request.user.student.semester
            branch=request.user.student.branch
            q=Course.objects.filter(semester=semester,branch=branch)
            li=[]
            for k in q:
                li.append(k.course_name)
            li=list(set(li))
            form=QueryFormRequest()
            return render(request,"makeaquery.html",{'li':li,'form':form})
        if request.method=="POST":
            if request.POST['question']=="":
                messages.info(request,"please fill something before submitting")
                return redirect("/studentlogin/student/makeaquery")
            else:
                to_who=request.POST['to_who']
                if to_who=="ADMIN":
                    question=request.POST['question']
                    send_status=1
                    from_stu=Student.objects.get(id=request.user.student.id)
                    to_adm=ADMIN.objects.all().first()
                    query=Query(question=question,send_status=send_status,from_stu=from_stu,to_adm=to_adm)
                    query.save()
                    messages.info(request,"query submitted successfully")
                    return redirect("/studentlogin/student/queries")

                else:
                    question=request.POST['question']
                    send_status=0
                    from_stu=Student.objects.get(id=request.user.student.id)
                    query=Query(question=question,send_status=send_status,from_stu=from_stu)
                    query.save()
                    c=Course.objects.filter(course_name=to_who)
                    for k in c:
                        query.to_course.add(k)
                        query.save()
                    messages.info(request,"query submitted successfully")
                    return redirect("/studentlogin/student/queries")
    def VIEWSTATS(self,request,coursename):
        q=Course.objects.filter(course_name=coursename).first().attendance_set.all()
        classesattended=0
        totalclasses=0
        for a in q:
            classesattended=classesattended+a.attended_classes_count
            totalclasses=totalclasses+a.total_classes_count
        totalclassaverage=int((classesattended/totalclasses)*100)
        obj=None
        for k in q:
            if k.stud.user.username==request.user.username:
                obj=k
                break
        print(obj)
        percentage=int((obj.attended_classes_count/obj.total_classes_count)*100)
        print(percentage)
        li=obj.absentdates.filter(attendanceid=obj.id)
        print(li)
        return render(request,"progressbar.html",{'obj':obj,'percentage':percentage,'li':li,'coursename':coursename,'student':request.user.student,'classavg':totalclassaverage})
    def find(self,details,request):
        image_data=request.POST.get("content").split(",")[1]
        print("hjsbdvhjsjdbvjsdbvjb")
        name=request.user.username
        with open(name+'.png','wb') as f:
                f.write(base64.b64decode(image_data))
        print(os.path.isfile(name+".png"))
        unknown_image=face_recognition.load_image_file(name+'.png')
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)
        if len(unknown_face_encoding) > 0:
                    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

        else:
                   print("No faces (or) Multiple faces found in the image!")
                   os.remove(name+".png")
                   return "USERNOTFOUND"
        
        known_face_encodings = []
        

        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # os.chdir("..")
        base_dir = os.getcwd()
        image_dir = os.path.join(base_dir,"{}\{}\{}\{}".format('media','Student_Images',details['semester'],details['branch']))
        print(image_dir)
       
        # print(image_dir)
        
        known_face_names = []
        p='Student_Images/{}/{}/{}'.format(request.user.student.semester,request.user.student.branch,request.user.username)
        path=os.path.join(BASE_DIR,"media/"+p)
        print(path)
        print(request.user.username)
        if os.path.isfile(path+'.png'):
                img = face_recognition.load_image_file(path+'.png')
                img_encoding = face_recognition.face_encodings(img)[0]
                result = face_recognition.compare_faces([img_encoding], unknown_face_encoding)
                if result[0]==True:
                        os.remove(name+".png")
                        return "USERFOUND"
                else:
                    os.remove(name+".png")
                    return "USERNOTFOUND"
        if os.path.isfile(path+'.jpeg'):
                img = face_recognition.load_image_file(path+'.jpeg')
                img_encoding = face_recognition.face_encodings(img)[0]
                result = face_recognition.compare_faces([img_encoding], unknown_face_encoding)
                if result[0]==True:
                        os.remove(name+".png")
                        return "USERFOUND"
                else:
                    os.remove(name+".png")
                    return "USERNOTFOUND"
        if os.path.isfile(path+'.jpg'):
                img = face_recognition.load_image_file(path+'.jpg')
                img_encoding = face_recognition.face_encodings(img)[0]
                result = face_recognition.compare_faces([img_encoding], unknown_face_encoding)
                if result[0]==True:
                        os.remove(name+".png")
                        return "USERFOUND"
                else:
                    os.remove(name+".png")
                    return "USERNOTFOUND"
        

        for root,dirs,files in os.walk(image_dir):
                for file in files:
                        if file.endswith('jpg') or file.endswith('png'):
                                path = os.path.join(root, file)
                                img = face_recognition.load_image_file(path)
                                label = file[:len(file)-4]
                                img_encoding = face_recognition.face_encodings(img)[0]
                                known_face_names.append(label)
                                known_face_encodings.append(img_encoding)
                        if file.endswith('jpeg'):
                                path = os.path.join(root, file)
                                img = face_recognition.load_image_file(path)
                                label = file[:len(file)-5]
                                img_encoding = face_recognition.face_encodings(img)[0]
                                known_face_names.append(label)
                                known_face_encodings.append(img_encoding)
        for j in known_face_encodings:
                result = face_recognition.compare_faces([j], unknown_face_encoding)
                if result[0]==True:
                        os.remove(name+".png")
                        print(known_face_names[known_face_encodings.index(j)])
                        print(request.user.username)

                        if known_face_names[known_face_encodings.index(j)]==request.user.username:
                                return "USERFOUND"
                        else:
                                return "USERNOTFOUND"
        os.remove(name+".png")
        return "USERNOTFOUND"
    def MARKATTENDANCE(self,request):
        if request.method=="GET":
                a=Student.objects.get(id=request.user.student.id)
                semester=a.semester
                branch=a.branch
                ob=None
                obj=a.attendance_set.all()
                for j in obj:
                        if j.cour.filter(attendance_taking_status=True).exists():
                                ob=j
                                break
                if Course.objects.filter(semester=semester,branch=branch,attendance_taking_status=True).exists() and ob.attended_status==False:
                        name=Course.objects.filter(semester=semester,branch=branch,attendance_taking_status=True).first().course_name
                        return render(request,'markattendance.html',{'name':name})
                else:
                        messages.info(request,"no subject is ongoing or ur attendance is noted")
                        return redirect("/studentlogin/student")


        if request.method=="POST":
                if Course.objects.filter(semester=request.user.student.semester,branch=request.user.student.branch,attendance_taking_status=True).exists():
                        a=Student.objects.get(id=request.user.student.id)
                        ob=None
                        obj=a.attendance_set.all()
                        for j in obj:
                                if j.cour.filter(attendance_taking_status=True).exists():
                                        ob=j
                                        break
                        details = {
                        'branch':request.user.student.branch,
                        'semester': request.user.student.semester
            
                        }
                #names = Recognizer(details)
                #students=Student.objects.filter(semester=request.user.student.semester,branch=request.user.student.branch)
                #flag=0
                #for student in students:
                        #if student.user.username==names:
#                               # break
                        s=a.find(details,request)
                        print(s)
                        if s=="USERFOUND":
                                ob.attended_status=True
                                ob.code=''
                                ob.attended_classes_count=ob.attended_classes_count+1
                                ob.save()
                                return JsonResponse({'success':'FOUND'})
                        else:
                                return JsonResponse({'success':'NOTFOUND'})
                else:
                        messages.info(request,"sorry time is over,attendance not noted")
                        return JsonResponse({'success':'timeover'})
                
                
                
                

                #if ob.code==request.POST['code']:
                       # ob.attended_status=True
                       # ob.code=''
                       # ob.attended_classes_count=ob.attended_classes_count+1
                       # ob.save()
                       # messages.info(request,"attendance noted")
                       # return redirect("/studentlogin/student")
                #if flag==1 :
                        #ob.attended_status=True
                        #ob.code=''
                        #ob.attended_classes_count=ob.attended_classes_count+1
                        #ob.save()
                        #messages.info(request,"attendance noted")
                        #return redirect("/studentlogin/student")
                #else:
                       # messages.info(request,"try again profile not found is wrong")
                        #return redirect("/studentlogin/student/markattendance")
               


from adminfunctionalities.forms import *
class ADMIN(models.Model):
        admin_user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
        def ADDNOTICE(self,request):
            if request.method=="GET":
                
             
                form=NoticeForm()
                return render(request,'addnotice.html',{'form':form})
            if request.method=="POST":
                if request.POST['Notice']=="":
                    messages.info(request,"please add notice before submitting")
                    return redirect("/adminlogin/admin/addnotice")
                else:

                    f=NoticeForm(request.POST)
                
                    f.save()
                
                    messages.info(request,"notice added successfully")
                    return redirect("/adminlogin/admin/addnotice")
        def DELETENOTICE(self,request):
            if request.method=="GET":
                obj=notices.objects.all()
                return render(request,'deletenotice.html',{'obj':obj})
            if request.method=="POST":
                querylist=request.POST.getlist('noticedelete')

                for i in querylist:
                    notices.objects.get(id=int(i)).delete()
                messages.info(request,"notices deleted successfully")
                return redirect("/adminlogin/admin/deletenotice")
       
        def GENERATEPASSWORD(self):
            s="0123456789"
            b=""
            for i in range(8):
                b=b+s[int(random.random()*10)]
            print(b)
            return b
        
        
        

        
        
        
        

        def ADDSTUDENT(self,request):
            if request.method=="GET":
                
                f=StudentForm()
                return render(request,'addstudent.html',{'form':f})
            if request.method=="POST":
                first_name=request.POST["firstname"]
                last_name=request.POST["lastname"]
                username=request.POST["id"]
                #password1=request.POST["password1"]
                #password2=request.POST["password2"]
                email=request.POST["email"]
                semester=request.POST["semester"]
                branch=request.POST["branch"]
                studprofilepic=request.FILES['studprofilepic']
                user=None
                #if password1==password2:
                if 1>0:
                    if not User.objects.filter(username=username).exists():
                        if not User.objects.filter(email=email).exists():
                            unknown_image=face_recognition.load_image_file(request.FILES['studprofilepic'])
                            unknown_face_encoding = face_recognition.face_encodings(unknown_image)
                            if len(unknown_face_encoding) <=0 :
           
                                messages.info(request,"No face (or) Multiple faces found,please fill again")
                                return redirect("/adminlogin/admin/addstudent")
                            details={
                                'semester':semester,
                                'branch':branch
                            }
                            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
                            base_dir = os.path.dirname(os.path.abspath(__file__))
      
                            base_dir = os.getcwd()
                            image_dir = os.path.join(base_dir,"{}\{}\{}\{}".format('media','Student_Images',details['semester'],details['branch']))
                            print(image_dir)
       
       
        
                            known_face_names = []
                            known_face_encodings=[]
                            for root,dirs,files in os.walk(image_dir):
                                for file in files:
                                    if file.endswith('jpg') or file.endswith('png') or file.endswith('jpeg') :
                                        path = os.path.join(root, file)
                                        img = face_recognition.load_image_file(path)
                                        if file.endswith('jpeg'):
                                            label = file[:len(file)-5]
                                        else:
                                            label = file[:len(file)-4]
                                        img_encoding = face_recognition.face_encodings(img)[0]
                                        known_face_names.append(label)
                                        known_face_encodings.append(img_encoding)
                            for j in known_face_encodings:
                                result = face_recognition.compare_faces([j], unknown_face_encoding)
                                if result[0]==True:
                                    messages.info(request,"this photo is already taken by  "+str(known_face_names[known_face_encodings.index(j)])+"kindly pleasse check and register again")

                                    return redirect("/adminlogin/admin/addstudent")

                            password1=self.GENERATEPASSWORD()
                            
                            subject = 'Do not reply'
                            
                          
                            message = 'Hi '+username+"   YOUR PASSWORD IS    "+password1
                            recipient_list = [email]
                            email_from = settings.EMAIL_HOST_USER
                            send_mail(subject,message, email_from, recipient_list )
           
                            
                            user=User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
                            user.save()
                            s=Student(user=user,semester=semester,branch=branch,studprofilepic=studprofilepic,spamprofilepic=studprofilepic)
                            s.save()
                            
                            c=Course.objects.filter(semester=semester,branch=branch)
                            li=[]
                            for k in c:
                                li.append(k.course_name)
                            li=list(set(li))
                            for j in li:
                                no=Course.objects.filter(course_name=j,semester=semester,branch=branch)
                                obj=Attendance(attended_classes_count=0,total_classes_count=0,code='',attended_status=False,stud=s)
                                obj.save()
                                for t in no:
                                    
                                    obj.cour.add(t)
                                    obj.save()

                            if Course.objects.filter(semester=semester,branch=branch).exists():
                                for i in Course.objects.filter(semester=semester,branch=branch):
                                    s.courses.add(i)
                                    s.save()
                        else:
                            messages.info(request,"email taken,please register again")
                            return redirect('/adminlogin/admin/addstudent')

                    else:
                        messages.info(request,"username Taken,please register again")
                        return redirect("/adminlogin/admin/addstudent")

        
                else:
                    #messages.info(request,"Passwords Not matching,Please Register again")
                    #return redirect("/adminlogin/admin/addstudent")
                    pass
                messages.info(request,"Student added Successfully")
                return redirect("/adminlogin/admin/addstudent")
        def ADDCOURSE(self,request):
            if request.method=='GET':
                
                f=CourseForm()
                return render(request,'addcourse.html',{'form':f})
            if request.method=="POST":
                if request.POST["course_syllabus"]=='':
                    messages.info(request,"please add course syllabus before submitting")
                    return redirect("/adminlogin/admin/addcourse")
                else:

                #course_name=request.POST['course_name']

                #branch=request.POST['branch']
                #semester=request.POST['semester']
                #day=request.POST['day']
                #time=request.POST['time']
                #course_syllabus=request.POST['course_syllabus']
                #if Course.objects.filter(course_name=course_name).exists() and (Course.objects.filter(course_name=course_name).first().semester !=semester or Course.objects.filter(course_name=course_name).first().branch !=branch):
                #    messages.info(request,"course,semester,branch are not matching")
                #    return redirect("/adminlogin/admin/addcourse")
                #else:
                #    if Course.objects.filter(course_name=course_name,branch=branch,semester=semester,day=day,time=time).exists():
                #        messages.info(request,"Course already registered")
                    
                #        return redirect("/adminlogin/admin/addcourse")
                
                
                
                #    else:
                #        if Course.objects.filter(branch=branch,semester=semester,day=day,time=time).exists():
                #           messages.info(request,"spot already taken by another course")
                #           return redirect("/adminlogin/admin/addcourse")

                #        else:
                #            c=Course(course_name=course_name,branch=branch,semester=semester,day=day,time=time,course_syllabus=course_syllabus)
                #            c.save()
                #            if Student.objects.filter(semester=semester,branch=branch).exists():
                #               o=Student.objects.filter(semester=semester,branch=branch)
                #                for ob in o:
                #                    ob.courses.add(c)
                #                    ob.save()
                                
                #                print(Course.objects.get(course_name=course_name).student_set.all())
                #                messages.info(request,"course is scheduled successfully")
                #                return redirect("/adminlogin/admin/addcourse")
                #            else:
                #                return redirect("/adminlogin/admin/addcourse")
                
                    course_name=request.POST['course_name']
                    branch=request.POST['branch']
                    semester=request.POST['semester']
                    if Course.objects.filter(course_name=course_name).exists():
                        messages.info(request,"course already scheduled")
                        return redirect("/adminlogin/admin/addcourse")
                    else:
                        monlen=len(request.POST.getlist("MONDAY"))
                        tueslen=len(request.POST.getlist("TUESDAY"))
                        wedlen=len(request.POST.getlist("WEDNESDAY"))
                        thulen=len(request.POST.getlist("THURSDAY"))
                        frilen=len(request.POST.getlist("FRIDAY"))
                        li=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]
                        spots=dict()
                        f=0
                        flag=""
                        if monlen+tueslen+wedlen+thulen+frilen>0:
                            for i in li:
                                if len(request.POST.getlist(i))>0:
                                    for j in request.POST.getlist(i):
                                        if Course.objects.filter(semester=semester,branch=branch,day=i,time=j).exists():
                                            if i in spots:
                                                spots[i]=spots[i]+","+j
                                            else:
                                                spots[i]=j
                                            f=1
                                            continue
                                    

                                else:
                                    continue
                            if f==1:
                                for key in spots:
                                    flag=flag+key+"-"+spots[key]+","
                        
                                messages.info(request,"These spots are already taken:-"+flag+"all other spots are ok, please schedule again")
                                return redirect("/adminlogin/admin/addcourse")
                            else:
                                for i in li:
                                    if len(request.POST.getlist(i))>0:
                                        for j in request.POST.getlist(i):
                                                c=Course(course_name=course_name,branch=branch,semester=semester,day=i,time=j,course_syllabus=request.POST["course_syllabus"])
                                                c.save()
                                                if Student.objects.filter(semester=semester,branch=branch).exists():
                                                    o=Student.objects.filter(semester=semester,branch=branch)
                                                    for ob in o:
                                                        ob.courses.add(c)
                                                        obj=None
                                                        flag=0
                                                        if ob.attendance_set.all().exists():
                                                           for j in ob.attendance_set.all():
                                                               if j.cour.filter(course_name=course_name).exists():
                                                                   flag=1
                                                                   obj=j
                                                                   break

                                                        if flag==0:
                                                            obj=Attendance(attended_classes_count=0,total_classes_count=0,code='',attended_status=False,stud=ob)
                                                            obj.save()
                                                            obj.cour.add(c)
                                                            obj.save()
                                                        else:
                                                            obj.cour.add(c)
                                                        
                                                        ob.save()
                                messages.info(request,"course scheduled successfully")
                                return redirect("/adminlogin/admin/addcourse")
                        else:
                            messages.info(request,"select atleast one spot")
                            return redirect("/adminlogin/admin/addcourse")
                

        def ADDPROFESSOR(self,request):
            if request.method=='GET':
                l=[]
                q=Course.objects.all()
                for j in q:
                    l.append(j.course_name)
                l=list(set(l))
                return render(request,'addprofessor.html',{'l':l})
            if request.method=="POST":
                first_name=request.POST["firstname"]
                last_name=request.POST["lastname"]
                username=request.POST["professorid"]
                #password1=request.POST["password1"]
                #password2=request.POST["password2"]
                email=request.POST["email"]
                profprofilepic=request.FILES['profprofilepic']
                user=None
                k=""
                #if password1==password2:
                if len(request.POST.getlist('allcourses'))>0:
                    if not User.objects.filter(username=username).exists():
                        if not User.objects.filter(email=email).exists():
                            unknown_image=face_recognition.load_image_file(request.FILES['profprofilepic'])
                            unknown_face_encoding = face_recognition.face_encodings(unknown_image)
                            if len(unknown_face_encoding) <=0 :
           
                                messages.info(request,"No face (ort) Multiple faces found,please fill again")
                                return redirect("/adminlogin/admin/addprofessor")
                            
                            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
                            base_dir = os.path.dirname(os.path.abspath(__file__))
      
                            base_dir = os.getcwd()
                            image_dir = os.path.join(base_dir,"{}\{}".format('media','Faculty_Images'))
                            
       
       
        
                            known_face_names = []
                            known_face_encodings=[]
                            for root,dirs,files in os.walk(image_dir):
                                for file in files:
                                    if file.endswith('jpg') or file.endswith('png') or file.endswith('jpeg') :
                                        path = os.path.join(root, file)
                                        img = face_recognition.load_image_file(path)
                                        if file.endswith('jpeg'):
                                            label = file[:len(file)-5]
                                        else:
                                            label = file[:len(file)-4]
                                        img_encoding = face_recognition.face_encodings(img)[0]
                                        known_face_names.append(label)
                                        known_face_encodings.append(img_encoding)
                            for j in known_face_encodings:
                                result = face_recognition.compare_faces([j], unknown_face_encoding)
                                if result[0]==True:
                                    messages.info(request,"this photo is already taken by  "+str(known_face_names[known_face_encodings.index(j)])+"kindly pleasse check and register again")

                                    return redirect("/adminlogin/admin/addprofessor")
                            
                            password1=self.GENERATEPASSWORD()
                            
                            subject = 'Donot reply'
                            
                          
                            message = 'Hi'+username+"YOUR PASSWORD IS "+password1
                            recipient_list = [email]
                            email_from = settings.EMAIL_HOST_USER
                            send_mail(subject,message, email_from, recipient_list )
           
                            
                            user=User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name,is_staff=True,is_superuser=False)
                            user.save()
                            p=Professor(user=user,profprofilepic=profprofilepic,spamprofilepic=profprofilepic)
                            p.save()
                            q=request.POST.getlist('allcourses')
                            di=[]
                            k=""
                            print(q)
                            for obj in q:
                                if Course.objects.filter(course_name=obj).exists():
                                  
                                    if Course.objects.filter(course_name=obj).first().professor is None:
                                        x=Course.objects.filter(course_name=obj)
                                        print(x)
                                        for y in x:
                                            y.professor=p
                                            y.save()
                                    else:
                                        k=k+obj+'takenby'+Course.objects.filter(course_name=obj).first().professor.user.username+","
                                    
                                else:
                                    continue
                        else:
                            messages.info(request,"email taken,please register again")
                            return redirect('/adminlogin/admin/addprofessor')

                    else:
                        messages.info(request,"username Taken,please register again")
                        return redirect("/adminlogin/admin/addprofessor")

        
                else:
                    messages.info(request,"Please select atleast one checkbox")
                    return redirect("/adminlogin/admin/addprofessor")
                if k!='':
                    s="This courses are already taken:"+k+"for all other courses registered "
                    messages.info(request,s)
                    return redirect("/adminlogin/admin/addprofessor")
                else:
                    messages.info(request,"professor added  successfully")
                    return redirect("/adminlogin/admin/addprofessor")
        def REMOVESTUDENT(self,request):
            if request.method=='GET':
                obj=Student.objects.all()
                semesters=['1','2','3','4','5','6','7','8']
                branches=['CSE','ECE','ME','EE']
                return render(request,"removestudent.html",{'obj':obj,'semesters':semesters,'branches':branches})
            if request.method=='POST':
                if len(request.POST.getlist('removestudents'))>0:

                    listofpk=request.POST.getlist('removestudents')
                    for i in listofpk:
                        a=User.objects.get(id=Student.objects.get(id=int(i)).user.id)
                        sem=a.student.semester
                        bran=a.student.branch
                        name=a.username
                        s='Student_Images/{}/{}/{}'.format(sem,bran,name)
                        path=os.path.join(BASE_DIR,"media/"+s)
                        if os.path.isfile(path+'.png'):
                            os.remove(path+'.png')
                        if os.path.isfile(path+'.jpeg'):
                            os.remove(path+'.jpeg')
                        if os.path.isfile(path+'.jpg'):
                            os.remove(path+'.jpg')
                        
                        q=a.student.attendance_set.all()
                        for j in q:
                            j.absentdates.all().delete()

                        User.objects.filter(id=Student.objects.get(id=int(i)).user.id).delete()
                    return redirect("/adminlogin/admin/removestudent")

                    
                    




                    
                    
                    

                else:
                    
                    messages.info(request,"please select atleast one student")
                    return redirect("/adminlogin/admin/removestudent")
                    
        def REMOVEPROFESSOR(self,request):
            if request.method=="GET":
                k=Professor.objects.all()
              
                maindi=dict()

                for j in k:
                    li=[]
                    if j.course_set.all().exists():
                        for p in j.course_set.all():
                            li.append(p.course_name)
                    
                    li=list(set(li))
                    maindi[j]=li
                    
                    
                    
                return render(request,"removeprofessor.html",{'maindi':maindi})
            if request.method=="POST":
                if len(request.POST.getlist('removeprofessors'))>0:
                    querylist=request.POST.getlist('removeprofessors')

                    for i in querylist:
                        a=User.objects.get(id=Professor.objects.get(id=int(i)).user.id)
                      
                        name=a.username
                        s='Faculty_Images/{}'.format(name)
                        path=os.path.join(BASE_DIR,"media/"+s)
                        if os.path.isfile(path+'.png'):
                            os.remove(path+'.png')
                        if os.path.isfile(path+'.jpeg'):
                            os.remove(path+'.jpeg')
                        if os.path.isfile(path+'.jpg'):
                            os.remove(path+'.jpg')
                        
                        User.objects.filter(id=Professor.objects.get(id=int(i)).user.id).delete()
                    return redirect("/adminlogin/admin/removeprofessor")
                else:
                    messages.info(request,"please select atleast one option before submitting")
                    return redirect("/adminlogin/admin/removeprofessor")

        def UPDATESTUDENTINFO(self,request,name):
            if request.method=='GET':
                k=User.objects.get(username=name)
                a=k.student
                return render(request,"updatestudentinfo.html",{'k':k,'student':a})
            if request.method=='POST':
                a=User.objects.get(username=name).username
                b=User.objects.get(username=name).email
                if User.objects.filter(username=request.POST['studentid']).exists() and a!=request.POST['studentid']:
                        messages.info(request,"studentid already taken")
                        return redirect("/adminlogin/admin/updatestudentinfo/"+name)
                else:
                    if User.objects.filter(email=request.POST['email']).exists() and b!=request.POST['email']:
                            messages.info(request,"email already taken")
                            return redirect("/adminlogin/admin/updatestudentinfo/"+name)
                    else:

                        s=Student.objects.get(id=User.objects.get(username=name).student.id)
                        a=s.semester
                        b=s.branch
                        z=s.user.username
                        s.courses.clear()
                        s.save()
                        s.user.email=request.POST["email"]
                        s.semester=request.POST["semester"]
                        s.branch=request.POST["branch"]
                        s.user.username=request.POST["studentid"]
                        s.user.save()
                        s.save()
                        if a!=request.POST["semester"] or b!=request.POST["branch"]:
                            s.attendance_set.all().delete()
                            c=Course.objects.filter(semester=request.POST['semester'],branch=request.POST['branch'])
                            li=[]
                            for k in c:
                                li.append(k.course_name)
                            li=list(set(li))
                            for j in li:
                                no=Course.objects.filter(course_name=j,semester=request.POST['semester'],branch=request.POST['branch'])
                                obj=Attendance(attended_classes_count=0,total_classes_count=0,code='',attended_status=False,stud=s)
                                obj.save()
                                for t in no:
                                    
                                    obj.cour.add(t)
                                    obj.save()
                            s1='Student_Images/{}/{}/{}'.format(request.POST['semester'],request.POST['branch'],request.POST['studentid'])
                            path1=os.path.join(BASE_DIR,"media/"+s1+".png")
                            s2='Student_Images/{}/{}/{}'.format(a,b,z)
                            x='Student_Images/{}/{}'.format(request.POST['semester'],request.POST['branch'])
                            y=os.path.join(BASE_DIR,"media/"+x)

                            path2=os.path.join(BASE_DIR,"media/"+s2+".png")
                            path3=os.path.join(BASE_DIR,"media/"+s2+".jpg")
                            path4=os.path.join(BASE_DIR,"media/"+s2+".jpeg")
                            if os.path.isfile(path2):
                                if os.path.isdir(y):
                                    move(path2, path1, copy_function = copy2)
                                    s.studprofilepic=path1
                                    s.save()
                                else:
                                    os.mkdir(y)
                                    move(path2, path1, copy_function = copy2)
                                    s.studprofilepic=path1
                                    s.save()
                            if os.path.isfile(path3):
                                if os.path.isdir(y):
                                    move(path3, path1, copy_function = copy2)
                                    s.studprofilepic=path1
                                    s.save()
                                else:
                                    os.mkdir(y)
                                    move(path3, path1, copy_function = copy2)
                                    s.studprofilepic=path1
                                    s.save()
                            if os.path.isfile(path4):
                                if os.path.isdir(y):
                                    move(path4, path1, copy_function = copy2)
                                    s.studprofilepic=path1
                                    s.save()
                                else:
                                    os.mkdir(y)
                                    move(path4, path1, copy_function = copy2)
                                    s.studprofilepic=path1
                                    s.save()
                        print(s.studprofilepic.url)

                        for i in Course.objects.filter(semester=request.POST['semester'],branch=request.POST['branch']):
                            s.courses.add(i)
                            s.save()
                        if z!=request.POST['studentid'] and a==request.POST['semester'] and b==request.POST['branch']:
                            s='Student_Images/{}/{}/{}'.format(a,b,z)
                            path=os.path.join(BASE_DIR,"media/"+s)
                            old_name=path
                            s='Student_Images/{}/{}/{}'.format(a,b,request.POST['studentid'])
                            path=os.path.join(BASE_DIR,"media/"+s)
                            new_name=path

                            if os.path.isfile(old_name+'.png'):
                                os.rename(old_name+'.png', new_name+".png")
                            if os.path.isfile(old_name+'.jpeg'):
                                os.rename(old_name+".jpeg", new_name+".jpeg")
                            if os.path.isfile(old_name+'.jpg'):
                                os.rename(old_name+".jpg", new_name+".jpg")

                        messages.info(request,"updated successfully")
                        return redirect("/adminlogin/admin")
        def UPDATEPROFESSORINFO(self,request,name):
            if request.method=="GET":
                k=User.objects.get(username=name)
                q=k.professor.course_set.all()
                l=[]
                for i in q:
                    l.append(i.course_name)
                l=list(set(l))
                li=[]
                p=Course.objects.all()
                for j in p:
                    li.append(j.course_name)
                li=list(set(li))
                return render(request,"updateprofessorinfo.html",{'k':k,'l':l,'li':li})
            if request.method=="POST":
                a=User.objects.get(username=name).username
                b=User.objects.get(username=name).email
                if len(request.POST.getlist("allcourses")) >0:
                    if User.objects.filter(username=request.POST['professorid']).exists() and a!=request.POST['professorid']:
                        messages.info(request,"Professorid already taken")
                        return redirect("/adminlogin/admin/updateprofessorinfo/"+name)
                    
                    else:
                        if User.objects.filter(email=request.POST['email']).exists() and b!=request.POST['email']:
                            messages.info(request,"email already taken")
                            return redirect("/adminlogin/admin/updateprofessorinfo/"+name)
                        else:
                            p=Professor.objects.get(id=User.objects.get(username=name).professor.id)
                            p.course_set.clear()
                            p.save()
                            p.user.email=request.POST["email"]
                            p.user.username=request.POST["professorid"]
                            p.user.save()
                            p.save()
                            q=request.POST.getlist('allcourses')
                            print(q)
                            for obj in q:
                                if Course.objects.filter(course_name=obj).exists():
                                    x=Course.objects.filter(course_name=obj)
                                    print(x)
                                    for y in x:
                                        y.professor=p
                                        y.save()
                                else:
                                    continue
                            if a!=request.POST['professorid']:
                                s='Faculty_Images/{}'.format(a)
                                path=os.path.join(BASE_DIR,"media/"+s)
                                old_name=path
                                s='Faculty_Images/{}'.format(request.POST['professorid'])
                                path=os.path.join(BASE_DIR,"media/"+s)
                                new_name=path

                                if os.path.isfile(old_name+'.png'):
                                    os.rename(old_name+'.png', new_name+".png")
                                if os.path.isfile(old_name+'.jpeg'):
                                    os.rename(old_name+".jpeg", new_name+".jpeg")
                                if os.path.isfile(old_name+'.jpg'):
                                    os.rename(old_name+".jpg", new_name+".jpg")
                            messages.info(request,"Updated Successfully")
                            return redirect("/adminlogin/admin")

                else:
                    messages.info(request,"Courses not selected")
                    return redirect("/adminlogin/admin/updateprofessorinfo/"+name)
        def RESCHEDULECOURSE(self,request):
            if request.method=="GET":
                f=CourseForm()
                return render(request,"reschedulecourse.html",{'form':f})
            if request.method=="POST":
                course_name=request.POST['course_name']
                if Course.objects.filter(course_name=course_name).exists():
                    monlen=len(request.POST.getlist("MONDAY"))
                    tueslen=len(request.POST.getlist("TUESDAY"))
                    wedlen=len(request.POST.getlist("WEDNESDAY"))
                    thulen=len(request.POST.getlist("THURSDAY"))
                    frilen=len(request.POST.getlist("FRIDAY"))
                    li=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]
                    spots=dict()
                    sem=Course.objects.filter(course_name=course_name).first().semester
                    bran=Course.objects.filter(course_name=course_name).first().branch
                    f=0
                    flag=""
                    prof=Course.objects.filter(course_name=course_name).first().professor
                    att=Course.objects.filter(course_name=course_name).first().attendance_set.all()
                    if monlen+tueslen+wedlen+thulen+frilen>0:
                        for i in li:
                            if len(request.POST.getlist(i))>0:
                                
                                print(att)
                                Course.objects.filter(course_name=course_name,day=i).delete()
                                for j in request.POST.getlist(i):
                                    if Course.objects.filter(semester=sem,branch=bran,day=i,time=j).exists():
                                        if i in spots:
                                            spots[i]=spots[i]+","+j
                                        else:
                                            spots[i]=j
                                        f=1
                                        continue
                                    else:

                                        c=Course(course_name=course_name,semester=sem,branch=bran,day=i,time=j,professor=prof)
                                        c.save()
                                        s=Student.objects.filter(semester=sem,branch=bran)
                                        for stu in s:
                                            stu.courses.add(c)
                                            stu.save()
                                        for k in att:
                                            k.cour.add(c)
                                            
                                        
                            else:
                                continue

                        if f==1:
                            for key in spots:
                                flag=flag+key+"-"+spots[key]+","
                        
                            messages.info(request,"These spots are already taken:-"+flag+"all other spots are rescheduled successfully")
                            return redirect("/adminlogin/admin/reschedulecourse")




                        messages.info(request,"course rescheduled successfully")
                        return redirect("/adminlogin/admin/reschedulecourse")
                    else:
                        messages.info(request,"select atleast one spot")
                        return redirect("/adminlogin/admin/reschedulecourse")
                else:
                    messages.info(request,"course not found")
                    return redirect("/adminlogin/admin/reschedulecourse")
        
        def SHOWTIMETABLE(self,request,branch,semester):
            a=Course.objects.filter(branch=branch,semester=semester)
            monday=dict()
            tuesday=dict()
            wednesday=dict()
            thursday=dict()
            friday=dict()
            br=branch
            sem=semester
            li=[monday,tuesday,wednesday,thursday,friday]
            for k in a:
                if k.day=="MONDAY":
                    monday[k.time]=k.course_name
                if k.day=="TUESDAY":
                    tuesday[k.time]=k.course_name
                if k.day=="WEDNESDAY":
                    wednesday[k.time]=k.course_name
                if k.day=="THURSDAY":
                    thursday[k.time]=k.course_name
                if k.day=="FRIDAY":
                    friday[k.time]=k.course_name
            di={'h':10}
            for i in li:
                if "10:00-11:00" not in i:
                    i["a"]="-"
                else:
                    p=i["10:00-11:00"]
                    del i["10:00-11:00"]
                    i["a"]=p
                if "11:00-12:00" not in i:
                    i["b"]="-"
                else:
                    p=i["11:00-12:00"]
                    del i["11:00-12:00"]
                    i["b"]=p
                if "14:00-15:00" not in i:
                    i["c"]="-"
                else:
                    p=i["14:00-15:00"]
                    del i["14:00-15:00"]
                    i["c"]=p
                if "15:00-16:00" not in i:
                    i["d"]="-"
                else:
                    p=i["15:00-16:00"]
                    del i["15:00-16:00"]
                    i["d"]=p
            
            print(monday)
            return render(request,"spotstimetable.html",{'branch':br,'semester':sem,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'di':di})


        def QUERIESFROMSTUDENTS(self,request):
            if request.method=='GET':
                q=Query.objects.filter(send_status=1,answered_status=False)
                return render(request,"queriesfromstudents.html",{'q':q})
        def QUERIESFROMSTUDENTSANDRESPOND(self,request,id):
            if request.method=="GET":
                question=Query.objects.get(id=id).question
                f=QueryFormResponse()
                return render(request,"respondtoqueriesfromstudents.html",{'question':question,'form':f})
            if request.method=="POST":
                if request.POST['answer']=="":
                    messages.info(request,"pleaserespond")
                    return redirect("/adminlogin/admin/queriesfromstudents/"+str(id))
                else:
                    q=Query.objects.get(id=id)
                    q.answered_status=True
                    q.answer=request.POST['answer']
                    q.save()
                    messages.info(request,"response submitted")
                    return redirect("/adminlogin/admin/managequeries")
        
        def QUERIESFROMPROFESSORS(self,request):
            if request.method=='GET':
                q=Query.objects.filter(send_status=2,answered_status=False)
                d=dict()
                for i in q:
                    li=[]
                    se=i.from_prof.course_set.all()
                    for j in se:
                        li.append(j.course_name)
                    li=list(set(li))

                    d[i]=li
                return render(request,"queriesfromprofessors.html",{'d':d})
        def QUERIESFROMPROFESSORSANDRESPOND(self,request,id):
            if request.method=="GET":
                question=Query.objects.get(id=id).question
                f=QueryFormResponse()
                return render(request,"resquefromprof.html",{'question':question,'form':f})
            if request.method=="POST":
                if request.POST['answer']=="":
                    messages.info(request,"pleaserespond")
                    return redirect("/adminlogin/admin/queriesfromprofessors/"+str(id))
                else:
                    q=Query.objects.get(id=id)
                    q.answered_status=True
                    q.answer=request.POST['answer']
                    q.save()
                    messages.info(request,"response submitted")
                    return redirect("/adminlogin/admin/managequeries")