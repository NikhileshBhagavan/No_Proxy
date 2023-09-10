from django import forms

from home.models import *
from .models import *

class NoticeForm(forms.ModelForm):
    class Meta:
        model=notices
        fields="__all__"
        widgets = {
            'Notice': forms.Textarea(attrs={'placeholder': '    Add a Notice'}),
            
        }
class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['semester','branch']

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['course_name','branch','semester','day','time','course_syllabus']
        widgets = {
            'course_syllabus': forms.Textarea(attrs={'placeholder': '    Please enter the syllabus course here'}),
            
        }
 